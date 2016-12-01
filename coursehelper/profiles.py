from database import get_db, query_db
from sqlite3 import IntegrityError, Row
from navigation import dict_factory

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


def getUserPosts(username):
	userPosts = []
	db = get_db()
	db.row_factory = dict_factory

	#print "Checking the courses user: " + username + " follows"
	
	postsFound = query_db('SELECT * FROM posts WHERE userid = (?)', (username, ) , one=False)

	if not postsFound is None:
			for post in postsFound:
				userPosts.append(post)

	#print "returning: " + str(convertToString(coursesFollowed))
	return userPosts


def getUserReviews(username):
	userReviews = []
	db = get_db()
	db.row_factory = dict_factory

	#print "Checking the courses user: " + username + " follows"
	
	reviewsFound = query_db('SELECT * FROM reviews WHERE userid = (?)', (username, ) , one=False)

	if not reviewsFound is None:
			for review in reviewsFound:
				userReviews.append(review)

	#print "returning: " + str(convertToString(coursesFollowed))
	return userReviews


def getUserResources(username):
	userResources = []
	db = get_db()
	db.row_factory = dict_factory

	#print "Checking the courses user: " + username + " follows"
	
	resourcesFound = query_db('SELECT * FROM resources WHERE userid = (?)', (username, ) , one=False)

	if not resourcesFound is None:
			for resource in resourcesFound:
				userResources.append(resource)

	#print "returning: " + str(convertToString(coursesFollowed))
	return userResources


def getFollowedUsers(username):
	usersFollowed = []
	db = get_db()
	db.row_factory = dict_factory

	#print "Checking the courses user: " + username + " follows"
	
	usersFound = query_db('SELECT * FROM userfollowers WHERE userid = (?)', (username, ) , one=False)

	if not usersFound is None:
			for user in usersFound:
				usersFollowed.append(user)

	#print "returning: " + str(convertToString(coursesFollowed))
	return usersFollowed
	

def followUserAttempt(request, session):
	follow = request.form['wantstofollow']
	followedUser = formatQuery(request.form['followeduser'])
	username = session['username']

	error = None
	
	try:
		db = get_db()

		if follow == "true":
			db.execute('INSERT INTO userfollowers (userid, followeduser) VALUES (?, ?)', [username, followedUser])
			db.commit()
		else:
			db.execute('DELETE FROM userfollowers WHERE userid=? AND followeduser=?', [username, followedUser])
			db.commit()
	except Error:
		db.rollback()
		error = "Invalid attempt!"
		print error

	return error

