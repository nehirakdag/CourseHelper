import registerlogin
import navigation
import datetime

from coursehelper import app
from flask import redirect, render_template, url_for, abort, flash, request, session


@app.route('/')
def index():
    print 'hello'
    if session.get('logged_in'):
        return render_template("loggedin_home.html", username=session['username'])

    return render_template("index.html")


@app.route('/register')
def registration():
    return render_template("register.html")


@app.route('/add', methods=['GET', 'POST'])
def user_Registration():
    #error = None
    if session.get('logged_in'):
        return render_template("loggedin_home.html", username=session['username'])

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
    if request.method == 'POST':

        # Attempt to call the login routine with the current request, session elements
        error = registerlogin.loginAttempt(request, session)

        # Render appropriate page depending on the response
        if not error is None:
            return render_template("index.html", error=error)
        else:
            return render_template("loggedin_home.html", username=session['username'])
    else:
        return render_template("index.html", error=None)


# If user wants to logout, remove the logged_in entry from their session
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    print "Logout successful"
    return redirect(url_for('index'))


@app.route('/courses/<courseid>/')
def coursepage(courseid):
    print "TESTTTTT"
    print courseid
    if not courseid.strip():
        return render_template("loggedin_home.html", username=session['username'])
    #print "Course ID is = " + courseid

    # Lookup the database for the passed query
    courseInfo = navigation.getCourseInfo(courseid)

    #print courseInfo

    # If no course was found, return user to their main profile page
    if not courseInfo:
        return render_template("loggedin_home.html", username=session['username'])

    # If a valid course was entered, fetch the posts associated with it and render its page
    else:
        coursePosts = navigation.getCoursePosts(courseid)
        isFollowing = navigation.checkIfFollowing(courseid, session['username'])

        return render_template("coursepg.html", courseid=courseInfo['name'], coursetitle=courseInfo['title'], coursedesc=courseInfo['description'], posts=coursePosts, following=isFollowing)

    return render_template("loggedin_home.html", username=session['username'])


@app.route('/addpost', methods=['GET', 'POST'])
def addPost():
    print 'TEST'

    if request.method == 'POST':
        error = navigation.addPostAttempt(request, session)
        courseid = request.form['courseid']
        #print "Course name is: " + courseid

        # add error handling?
        return redirect(url_for('coursepage', courseid=courseid))

    else:
        return render_template("loggedin_home.html", username=session['username'])


@app.route('/courses/<courseid>/reviews')
def reviewspage(courseid):
    
    courseInfo = navigation.getCourseInfo(courseid)

    #print courseInfo

    # If no course was found, return user to their main profile page
    if not courseInfo:
        return render_template("loggedin_home.html", username=session['username'])

    # If a valid course was entered, fetch the posts associated with it and render its page
    else:
        coursePosts = navigation.getCoursePosts(courseid)
        return render_template("reviews.html", courseid=courseInfo['name'], coursetitle=courseInfo['title'], coursedesc=courseInfo['description'])


@app.route('/followcourse', methods=['GET', 'POST'])
def followCourse():

    if request.method == 'POST':
        error = navigation.followCourseAttempt(request, session)
        
        courseid = request.form['courseid']
        #print "Course name is: " + courseid

        # add error handling?
        return redirect(url_for('coursepage', courseid=courseid))

    else:
        return render_template("loggedin_home.html", username=session['username'])




