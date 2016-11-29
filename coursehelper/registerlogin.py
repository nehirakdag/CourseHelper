import bcrypt
import re

from database import get_db, query_db
from sqlite3 import IntegrityError, Row

EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")

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
    elif not EMAIL_REGEX.match(email):
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

def registerAttempt(request):
    db = get_db()

    userName = str(request.form['user'])
    passwd = str(request.form['pass'])
    passwdConf = str(request.form['pwConf'])
    email = str(request.form['email'])
    
    #Check if the attempted query is properly formatted
    error = checkForCorrectRegistration(userName, passwd, passwdConf, email)
    # Check if an error was encountered so far
    if not error is None:
        print error
        return error

    #hashedPassword = bcrypt.hashpw(passwd, bcrypt.gensalt())
    checkPass = bytes(passwd).encode('utf-8')
    hashedPassword = str(bcrypt.hashpw(checkPass, bcrypt.gensalt())).encode('utf-8')
    
    #Check if entered username was unique
    try:
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [userName , email, hashedPassword])
        db.commit()
    #if not, redirect user to registration page
    except IntegrityError:
        db.rollback()
        error = "Invalid Username! Please specify a unique username"
        print error
        return error

def loginAttempt(request, session):
    error = None

    db = get_db()
    db.row_factory = Row

    # Collect the fields from the form to reduce database interaction time
    userName = str(request.form['user'])
    passwd = str(request.form['pass'])

    # Check if attempted query is properly formatted
    error = checkForCorrectLogin(userName, passwd, error)

    # Check if an error was encountered so far
    if not error is None:
        print error
        return error

    # Retrieve the specified user's information from the database
    userInfo = query_db('SELECT * FROM users WHERE username = ?', (userName, ) , one=True)

    # Check if the user exists
    if userInfo is None:
        error = "Error! Username does not exist"
    else:
        # Check if the password matches the entry on the database
        checkPass = bytes(passwd).encode('utf-8')
        hashedPassword = bytes(userInfo['password']).encode('utf-8')

        if bcrypt.hashpw(checkPass, hashedPassword) != hashedPassword:
            error = "Error! Wrong password!"

    # Check if an error was encountered so far
    if not error is None:
        print error
        return error

    # Login succesfull. Set the appropriate session entries and send the user to their entry page
    session['logged_in'] = True
    session['username'] = userName

    return error



