import registerlogin
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


@app.route('/courses/<courseid>')
def coursepage(courseid):
    posts = []
    post = {}
    post['user'] = 'xxx'
    post['post'] = "Does anyone know what textbook chapters we need for the midterm?"
    post['timestamp'] = datetime.date.today()
    posts.append(post)
    return render_template("coursepg.html", courseid=courseid, coursetitle="Principles of Web Development",
        coursedesc='''Computer Science (Sci) : The course discusses the major principles, algorithms,
        languages and technologies that underlie web development. Students receive practical 
        hands-on experience through a project.''', posts=posts)
