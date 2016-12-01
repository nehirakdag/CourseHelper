import registerlogin
import navigation
import upload
import profiles

from coursehelper import app
from flask import redirect, render_template, url_for, abort, flash, request, session


@app.route('/')
def index():
    if session.get('logged_in'):
        username = session['username']

        coursesFollowed = profiles.getCoursesFollowed(username)
        userPosts = profiles.getUserPosts(username)
        userReviews = profiles.getUserReviews(username)
        userResources = profiles.getUserResources(username)
        followedUsers = profiles.getFollowedUsers(username)

        return render_template("homepage.html", username=username, courses=coursesFollowed, posts=userPosts, reviews=userReviews, resources=userResources)

    return render_template("index.html")


@app.route('/register')
def registration():
    if not session.get('logged_in'):
        return render_template("register.html")


@app.route('/add', methods=['GET', 'POST'])
def user_Registration():
    #error = None
    if not request.method == 'POST' or session.get('logged_in'):
        return redirect(url_for('index'))

    # Call the register routine with the current request element
    error = registerlogin.registerAttempt(request)

    # Render appropriate page depending on the response
    if not error is None:
        return render_template("register.html", error=error)
    else:
        return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Only POST requests can perform succesfull login attempts
    if request.method == 'POST' and not session.get('logged_in'):

        # Attempt to call the login routine with the current request, session elements
        error = registerlogin.loginAttempt(request, session)

        # Render appropriate page depending on the response
        if not error is None:
            return render_template("index.html", error=error)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# If user wants to logout, remove the logged_in entry from their session
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    print "Logout successful"
    return redirect(url_for('index'))


@app.route('/courses/<courseid>/')
def coursepage(courseid):
    if not courseid.strip():
        return redirect(url_for('index'))

    # Lookup the database for the passed query
    courseInfo = navigation.getCourseInfo(courseid)

    # If no course was found, return user to their main profile page
    if not courseInfo or not session.get('logged_in'):
        #check if this is a user instead:
        if navigation.checkIfUserExists(courseid):
            return redirect(url_for('profilePage', userid=courseid))
        return redirect(url_for('index'))

    # If a valid course was entered, fetch the posts associated with it and render its page
    else:
        coursePosts = navigation.getCoursePosts(courseid)
        isFollowing = navigation.checkIfFollowing(courseid, session['username'])

        return render_template("coursepg.html", viewer=session['username'], courseid=courseInfo['name'], coursetitle=courseInfo['title'], coursedesc=courseInfo['description'], posts=coursePosts, following=isFollowing)

    return redirect(url_for('index'))


@app.route('/addpost', methods=['GET', 'POST'])
def addPost():

    if request.method == 'POST' and session.get('logged_in'):
        error = navigation.addPostAttempt(request, session)
        courseid = request.form['courseid']
        #print "Course name is: " + courseid

        # add error handling?
        return redirect(url_for('coursepage', courseid=courseid))

    else:
        return redirect(url_for('index'))


@app.route('/courses/<courseid>/reviews')
def reviewspage(courseid):
    
    courseInfo = navigation.getCourseInfo(courseid)
    #print courseInfo

    # If no course was found, return user to their main profile page
    if not courseInfo or not session.get('logged_in'):
        return redirect(url_for('index'))

    # If a valid course was entered, fetch the posts associated with it and render its page
    else:
        courseReviews = navigation.getCourseReviews(courseid)
        isFollowing = navigation.checkIfFollowing(courseid, session['username'])
        return render_template("reviews.html", viewer=session['username'], courseid=courseInfo['name'], coursetitle=courseInfo['title'], coursedesc=courseInfo['description'], reviews=courseReviews, following=isFollowing)


@app.route('/followcourse', methods=['GET', 'POST'])
def followCourse():

    if request.method == 'POST' and session.get('logged_in'):
        error = navigation.followCourseAttempt(request, session)
        courseid = request.form['courseid']

        # add error handling?
        pageName = request.form['pageName']

        return redirect(url_for(pageName, courseid=courseid))

    else:
        return redirect(url_for('index'))


@app.route('/followuser', methods=['GET', 'POST'])
def followUser():

    if request.method == 'POST' and session.get('logged_in'):
        error = profiles.followUserAttempt(request, session)
        #profile = request.form['profile']

        #return redirect(url_for('profilePage', userid=profile))
        return redirect(url_for('profilePage', userid=session['username']))
    else:
        return redirect(url_for('index'))


@app.route('/addreview', methods=['GET', 'POST'])
def addReview():

    if request.method == 'POST' and session.get('logged_in'):
        error = navigation.addReviewAttempt(request, session)
        courseid = request.form['courseid']
        #print "Course name is: " + courseid

        # add error handling?
        return redirect(url_for('reviewspage', courseid=courseid))

    else:
        return redirect(url_for('index'))


@app.route('/profiles/<userid>/')
def profilePage(userid):

    # Viewer must be logged in to attempt to view a profile
    if session.get('logged_in') and navigation.checkIfUserExists(userid):

        if session['username'] == userid:
            return redirect(url_for('index'))
        else:

            coursesFollowed = profiles.getCoursesFollowed(userid)
            userPosts = profiles.getUserPosts(userid)
            #userReviews = profiles.getUserReviews(username)
            userResources = profiles.getUserResources(userid)
            followedUsers = profiles.getFollowedUsers(userid)
            
            return render_template("profile.html", username=userid, courses=coursesFollowed, posts=userPosts, resources=userResources)

    return redirect(url_for('index'))


@app.route('/deletepost', methods=['GET', 'POST'])
def deletePost():

    # Must be a POST request to actually delete a post
    if request.method == 'POST' and session.get('logged_in'):
        error = navigation.deletePostAttempt(request, session)

        if not error is None:
            return redirect(url_for('index'))
        else:
            courseid = request.form['courseid']
        return redirect(url_for('coursepage', courseid=courseid))

    return redirect(url_for('index'))

@app.route('/deletereview', methods=['GET', 'POST'])
def deleteReview():

    # Must be a POST request to actually delete a post
    if request.method == 'POST' and session.get('logged_in'):
        error = navigation.deleteReviewAttempt(request, session)

        if not error is None:
            return redirect(url_for('index'))
        else:
            courseid = request.form['courseid']
        return redirect(url_for('reviewspage', courseid=courseid))

    return redirect(url_for('index'))


@app.route('/courses/<courseid>/resources')
def resourcespage(courseid):

    courseInfo = navigation.getCourseInfo(courseid)
    #print courseInfo

    # If no resource was found, return user to their main profile page
    if not courseInfo or not session.get('logged_in'):
        return redirect(url_for('index'))

    # If a valid resource was entered, fetch the components associated with it and render its page
    else:
        courseResources = navigation.getCourseResources(courseid)
        isFollowing = navigation.checkIfFollowing(courseid, session['username'])
        return render_template("resources.html", courseid=courseInfo['name'], coursetitle=courseInfo['title'], coursedesc=courseInfo['description'], resources=courseResources, following=isFollowing)

@app.route('/uploadresource', methods=['GET', 'POST'])
def uploadResource():

    if request.method == 'POST' and session.get('logged_in'):
        error = None

        courseid = request.form['courseid']

        if 'file[]' not in request.files:
            error = "No file entered"
            return redirect(url_for('resourcespage', courseid=courseid))

        uploadAttempt = upload.uploadFilesAttempt(request, session)
            
        return redirect(url_for('resourcespage', courseid=courseid))

    return redirect(url_for('index'))




