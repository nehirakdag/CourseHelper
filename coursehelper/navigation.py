import re
import yaml
import datetime
import sqlite3
import collections

from database import get_db, query_db
from sqlite3 import IntegrityError, Row

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def convertToString(data):
	if isinstance(data, basestring):
		return str(data)
	elif isinstance(data, collections.Mapping):
		return dict(map(convertToString, data.iteritems()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convertToString, data))
	else:
		return data


def regexCheck(searchQuery):
	return re.match(r'^[a-zA-Z]{4}\s?[0-9]{3}([a-zA-Z]\d)?$', searchQuery)

def formatQuery(searchQuery):
	query = (searchQuery.upper()).replace(" ", "")
	qLength = len(query)

	if qLength > 7:
		query = query[:-(qLength - 7)]

	return query

def getCourseInfo(courseID):
	courseInfo = {}

	if regexCheck(courseID):
		query = formatQuery(courseID)
		#print "Searching for : " + query

		db = get_db()
		db.row_factory = Row

		result = query_db('SELECT * FROM courses WHERE courseid = (?)', (query, ) , one=True)
		
		if not result is None:
			courseInfo = yaml.safe_load(result['description'])

	return courseInfo

def getCoursePosts(courseID):
	coursePosts = []

	if regexCheck(courseID):
		query = formatQuery(courseID)
		#print "Asking for posts for course: " + query 
		
		db = get_db()
		db.row_factory = dict_factory

		result = query_db('SELECT * FROM posts WHERE courseid = (?)', (query, ) , one=False)

		#print "Received: " + str(result)

		if not result is None:
			for desc in result:
				#print "checking : " + str(desc)
				coursePosts.append(desc)

	return coursePosts

def checkValidPost(post):
	error = None

	if len(post) < 2:
		error = "Error! Post must contain at least 3 characters"

	return error

def checkValidReview(review):
	error = None

	if len(review) < 5:
		error = "Error! Post must contain at least 5 characters"

	return error

def addPostAttempt(request, session):
	post = request.form['post']
	courseid = formatQuery(request.form['courseid'])
	#print "Wants to add Post: " + post + " to Course : " + courseid

	error = checkValidPost(post)

	if not error is None:
		print error
		return error

	username = session['username']
	timestamp = datetime.datetime.now().strftime("%H:%M %Y-%m-%d")
	db = get_db()

	try:
		db.execute('INSERT INTO posts (userid, courseid, post, tstamp) VALUES (?, ?, ?, ?)', [username, courseid, post, timestamp])
		db.commit()
    #if not, redirect user to registration page
	except IntegrityError:
		db.rollback()
		error = "Invalid Entry!"
		print error
		return error

	return error


def followCourseAttempt(request, session):
	follow = request.form['wantstofollow']
	courseid = formatQuery(request.form['courseid'])
	username = session['username']

	error = None
	
	try:
		db = get_db()

		if follow == "true":
			db.execute('INSERT INTO coursefollowers (userid, courseid) VALUES (?, ?)', [username, courseid])
			db.commit()
		else:
			db.execute('DELETE FROM coursefollowers WHERE userid=? AND courseid=?', [username, courseid])
			db.commit()
	except Error:
		db.rollback()
		error = "Invalid attempt!"
		print error

	return error


def checkIfFollowing(courseid, username):
	following = False
	db = get_db()

	checkCourse = formatQuery(courseid)

	#print "Checking if " + username + " follows course: " + checkCourse
	try:
		result = query_db('SELECT * FROM coursefollowers WHERE userid=(?) AND courseid=(?)', (username, checkCourse, ) , one=True)
		#print "Found: " + str(result)
		if not result is None:
			following = True

	except IntegrityError:
		db.rollback()

	return following


def getCoursesFollowed(username):
	coursesFollowed = []
	db = get_db()
	db.row_factory = dict_factory

	#print "Checking the courses user: " + username + " follows"
	
	coursesFound = query_db('SELECT * FROM coursefollowers WHERE userid = (?)', (username, ) , one=False)

	if not coursesFound is None:
			for course in coursesFound:
				coursesFollowed.append(course)

	#print "returning: " + str(convertToString(coursesFollowed))
	return coursesFollowed


def addReviewAttempt(request, session):
	review = request.form['review']
	courseid = formatQuery(request.form['courseid'])
	
	#print "Wants to add review: " + review + " to Course : " + courseid
	error = checkValidReview(review)

	if not error is None:
		print error
		return error

	username = session['username']
	timestamp = datetime.datetime.now().strftime("%H:%M %Y-%m-%d")
	stars = request.form['stars']
	#print "Stars is : " + str(stars)

	db = get_db()

	try:
		db.execute('INSERT INTO reviews (tstamp, courseid, userid, review, stars) VALUES (?, ?, ?, ?, ?)', [timestamp, courseid, username, review, stars])
		db.commit()
    #if not, redirect user to registration page
	except IntegrityError:
		db.rollback()
		error = "Invalid Entry!"
		print error
		return error

	return error


def getCourseReviews(courseID):
	courseReviews = []

	if regexCheck(courseID):
		query = formatQuery(courseID)
		#print "Asking for posts for course: " + query 
		
		db = get_db()
		db.row_factory = dict_factory

		result = query_db('SELECT * FROM reviews WHERE courseid = (?)', (query, ) , one=False)

		#print "Received: " + str(result)

		if not result is None:
			for desc in result:
				#print "checking : " + str(desc)
				courseReviews.append(desc)

	return courseReviews


def checkIfUserExists(username):
	exists = False

	db = get_db()
	userInfo = query_db('SELECT * FROM users WHERE username = ?', (username, ) , one=True)

	if not userInfo is None:
		exists = True

	return exists


def deletePostAttempt(request, session):
	username = session['username']
	postid = request.form['postid']
	error = None

	db = get_db()

	try:
		db.execute('DELETE FROM posts WHERE userid=? AND postid=?', [username, postid])
		db.commit()
	except IntegrityError:
		error = "Error! Invalid attempt"
		print error

	return error


def deleteReviewAttempt(request, session):
	username = session['username']
	reviewid = request.form['reviewid']
	error = None

	db = get_db()

	try:
		db.execute('DELETE FROM reviews WHERE userid=? AND reviewid=?', [username, reviewid])
		db.commit()
	except IntegrityError:
		error = "Error! Invalid attempt"
		print error

	return error


def getCourseResources(courseid):
	resource = {}
	resource['url'] = "lel"
	resource['name'] = "lil"

	return [resource]






