#import bcrypt
import registerlogin

from coursehelper import app
from flask import redirect, render_template, url_for, abort, flash, request, session
#from database import get_db, query_db
#from sqlite3 import IntegrityError, Row

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
    


    # db = get_db()

    # userName = str(request.form['user'])
    # passwd = str(request.form['pass'])
    # passwdConf = str(request.form['pwConf'])
    # email = str(request.form['email'])
    
    # #Check if the attempted query is properly formatted
    # error = checkForCorrectRegistration(userName, passwd, passwdConf, email)
    # # Check if an error was encountered so far
    # if not error is None:
    #     print error
    #     return render_template("register.html", error=error)

    # #hashedPassword = bcrypt.hashpw(passwd, bcrypt.gensalt())
    # checkPass = bytes(passwd).encode('utf-8')
    # hashedPassword = str(bcrypt.hashpw(checkPass, bcrypt.gensalt())).encode('utf-8')
    
    # #Check if entered username was unique
    # try:
    #     db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [userName , email, hashedPassword])
    #     db.commit()
    # #if not, redirect user to registration page
    # except IntegrityError:
    #     db.rollback()
    #     error = "Invalid Username! Please specify a unique username"
    #     print error
    #     return render_template("register.html", error=error)

    #print ('New entry was successfully posted')

    error = registerlogin.registerAttempt(request)

    if not error is None:
        return render_template("register.html", error=error)
    else:
        return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Only POST requests can perform succesfull login attempts
    if request.method == 'POST':
        # error = None

        # db = get_db()
        # db.row_factory = Row

        # # Collect the fields from the form to reduce database interaction time
        # userName = str(request.form['user'])
        # passwd = str(request.form['pass'])

        # # Check if attempted query is properly formatted
        # error = checkForCorrectLogin(userName, passwd, error)

        # # Check if an error was encountered so far
        # if not error is None:
        #     print error
        #     return render_template("index.html", error=error)

        # # Retrieve the specified user's information from the database
        # userInfo = query_db('SELECT * FROM users WHERE username = ?', (userName, ) , one=True)

        # # Check if the user exists
        # if userInfo is None:
        #     error = "Error! Username does not exist"
        # else:
        #     # Check if the password matches the entry on the database
        #     checkPass = bytes(passwd).encode('utf-8')
        #     hashedPassword = bytes(userInfo['password']).encode('utf-8')

        #     if bcrypt.hashpw(checkPass, hashedPassword) != hashedPassword:
        #         error = "Error! Wrong password!"

        # # Check if an error was encountered so far
        # if not error is None:
        #     print error
        #     return render_template("index.html", error=error)

        # # Login succesfull. Set the appropriate session entries and send the user to their entry page
        # session['logged_in'] = True
        # session['username'] = userName

        # return render_template("loggedin_home.html", username=session['username'])

        error = registerlogin.loginAttempt(request, session)

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
