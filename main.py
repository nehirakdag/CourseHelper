import os
import sqlite3
import re
import bcrypt

from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from contextlib import closing

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)
EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'courseHelper.db'),
    SECRET_KEY='comp307',
    USERNAME='admin',
    PASSWORD='default'
))
#app.config.from_envvar('COURSEHELPER_SETTINGS', silent=True)

@app.before_request
def before_request():
    g.db = connect_db()
    print 'initialized DB'

# Functions marked with teardown_appcontext are called every time the app context tears down
# A teardown happens either when after everything went well (app closes, error = None) or an exception occurred
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    print ("db closed")

def connect_db():
    # Connect to the database
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    # Open a database connection if and only if there is none yet, for the current application context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    #db = get_db()
    #with app.open_resource('schema.sql', mode='r') as f:
    #   db.cursor().executescript(f.read())
    #db.commit()
        with closing(connect_db()) as db:
                with app.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()

if not(os.path.exists(app.config['DATABASE'])):
    init_db()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
        
#@app.cli.command('initdb')
#def initdb_command():
    # Initializes the database
#   init_db()
#   print 'Initialized the database according to the schema'

@app.route('/')
def hello_world():
    print 'hello'
    if session.get('logged_in'):
        return render_template
    return render_template("index.html")

@app.route('/register')
def registration():
    return render_template("register.html")

# @app.route('/profiles')
# def show_entries():
#     db = get_db()
#     cur = db.execute('select username, password from entries order by id desc')
#     entries = cur.fetchall()
#     return render_template('profiles.html', entries=entries)

def checkForCorrectRegistration(username, password, passwordConf, email):
    error = None

    # Check if any of the fields were blank
    if not username.strip():
        error = "Error! Username can not be blank!"
    elif not password.strip() or not passwordConf.strip():
        error = "Error! Password can not be blank!"
    elif not email.strip():
        error = "Error! Email address can not be blank!"
    elif len(username) > 50:
        error = "Error! Username can not contain more than 50 characters"
    
    # Check if the two password entries match
    elif password != passwordConf:
        error = "Error! Password must match Password Confirmation"
    elif len(password) > 50:
        error = "Error! Password can not contain more than 50 characters"
    
    # Check if a valid email address was entered
    elif not EMAIL_REGEX.match(request.form['email']):
        error = "Error! Please input a valid email address"

    return error

def checkForCorrectLogin(username, password, currentError):
    error = currentError

    # Check if any of the fields were blank
    if not username.strip():
        error = "Error! Username can not be blank!"
    elif not password.strip():
        error = "Error! Password can not be blank!"
    
    # Check if input length was too large
    elif len(username) > 50:
        error = "Error! Username can not contain more than 50 characters"
    elif len(password) > 50:
        error = "Error! Password can not contain more than 50 characters"

    return error

@app.route('/add', methods=['GET', 'POST'])
def user_Registration():
    #error = None
    if session.get('logged_in'):
        flash('aborting!')
        abort(401)
    db = get_db()

    # print request.form['pass']
    # print request.form['pwConf']
    # Check if password entries match
    # if request.form['pass'] != request.form['pwConf']:
    #     error = "Error! Password must match Password Confirmation"
    #     print error
    #     return render_template("register.html", error=error)

    # # Check if a valid email address was entered
    # if not EMAIL_REGEX.match(request.form['email']):
    #     error = "Error! Please input a valid email address"
    #     print error
    #     return render_template("register.html", error=error)

    userName = str(request.form['user'])
    passwd = str(request.form['pass'])
    passwdConf = str(request.form['pwConf'])
    email = str(request.form['email'])
    
    error = checkForCorrectRegistration(userName, passwd, passwdConf, email)
    if not error is None:
        print error
        return render_template("register.html", error=error)

    #hashedPassword = bcrypt.hashpw(passwd, bcrypt.gensalt())
    checkPass = bytes(passwd).encode('utf-8')
    hashedPassword = str(bcrypt.hashpw(checkPass, bcrypt.gensalt())).encode('utf-8')
    
    #Check if entered username was unique
    try:
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [userName , email, hashedPassword])
        db.commit()
    #if not, redirect user to registration page
    except sqlite3.IntegrityError:
        db.rollback()
        error = "Invalid Username! Please specify a unique username"
        print error
        return render_template("register.html", error=error)

    #print ('New entry was successfully posted')
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None

        db = get_db()
        db.row_factory = sqlite3.Row

        userName = str(request.form['user'])
        passwd = str(request.form['pass'])

        userInfo = query_db('SELECT * FROM users WHERE username = ?', (userName, ) , one=True)

        if userInfo is None:
            error = "Error! Username does not exist"
        else:
            checkPass = bytes(passwd).encode('utf-8')
            hashedPassword = bytes(userInfo['password']).encode('utf-8')
            if bcrypt.hashpw(checkPass, hashedPassword) != hashedPassword:
                error = "Error! Wrong password!"

        error = checkForCorrectLogin(userName, passwd, error)
        if not error is None:
            print error
            return render_template("index.html", error=error)

        # if request.method == 'POST':
        #     if request.form['user'] != app.config['USERNAME']:
        #         error = 'Invalid username'
        #     elif request.form['pass'] != app.config['PASSWORD']:
        #         error = 'Invalid password'
        #     elif request.form['pass'] != request.form['pwConf']:
        #         error = 'Password and confirmation must match'
        #     else:
        #         session['logged_in'] = True
        #         flash('You were logged in')
        #         return redirect(url_for('show_entries'))

        session['logged_in'] = True
        return render_template("loggedin_home.html", username=str(request.form['user']))

    else:
        return render_template("index.html", error=None)

# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))