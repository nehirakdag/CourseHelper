import re
import yaml

from database import get_db, query_db
from sqlite3 import IntegrityError, Row

def regexCheck(searchQuery):
	return re.match(r'^[a-zA-Z]{4}\s?[0-9]{3}([a-zA-Z]\d)?$', searchQuery)

def formatQuery(searchQuery):
	query = (searchQuery.upper()).replace(" ", "")
	qLength = len(query)

	if qLength > 7:
		query = query[:-(qLength - 7)]

	return query

def getCourseInfo(courseID):
	print "TEST"
	courseInfo = {}

	if regexCheck(courseID):
		query = formatQuery(courseID)
		print "Searching for : " + query

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
		
		db = get_db()
		db.row_factory = Row

		result = query_db('SELECT * FROM posts WHERE courseid = (?)', (query, ) , one=False)

		if not result is None:
			for desc in result:
				post = yaml.safe_load(desc['post'])
				coursePosts.append(post)

	return coursePosts

