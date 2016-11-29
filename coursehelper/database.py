import os
import sqlite3
from coursehelper import app
from flask import g

#Connect to the database
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
    # Initializes the database according to the schema 
    with closing(connect_db()) as db:
        with app.open_resource('./db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()

# If the database file is not present in the desired location, create a new one
if not(os.path.exists(app.config['DATABASE'])):
    init_db()

# Function that allows any generic queries to be passed to the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

