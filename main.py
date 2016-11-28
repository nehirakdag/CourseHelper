import os
import sqlite3

from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap
from contextlib import closing

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

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

def connect_db():
	# Connect to the database
	#rv = sqlite3.connect(app.config['DATABASE'])
	#rv.row_factory = sqlite3.Row
	#return rv
	return sqlite3.connect(app.config['DATABASE'])

def get_db():
	# Open a database connection if and only if there is none yet, for the current application context
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	#db = get_db()
	#with app.open_resource('schema.sql', mode='r') as f:
	#	db.cursor().executescript(f.read())
	#db.commit()
        with closing(connect_db()) as db:
                with app.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()

if not(os.path.exists(app.config['DATABASE'])):
    init_db()
        
#@app.cli.command('initdb')
#def initdb_command():
	# Initializes the database
#	init_db()
#	print 'Initialized the database according to the schema'

# Functions marked with teardown_appcontext are called every time the app context tears down
# A teardown happens either when after everything went well (app closes, error = None) or an exception occurred
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
	print ("db closed")

@app.route('/')
def hello_world():
        print 'hello'
	return render_template("index.html")

@app.route('/register')
def registration():
	return render_template("register.html")

# @app.route('/profiles')
# def show_entries():
# 	db = get_db()
# 	cur = db.execute('select username, password from entries order by id desc')
# 	entries = cur.fetchall()
# 	return render_template('profiles.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def register_to_db():
    if session.get('logged_in'):
    	flash('aborting!')
        abort(401)
    db = get_db()
    print (request.form['pass'])

    #Check if entered username was unique
    try:
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [request.form['user'] , request.form['email'], request.form['pass']])
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        print "USERNAME MUST BE UNIQUE"
        return redirect(url_for('registration'))
    #print ('New entry was successfully posted')
    return redirect(url_for('hello_world'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['user'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['pass'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         elif request.form['pass'] != request.form['pwConf']:
#         	error = 'Password and confirmation must match'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)

# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))
