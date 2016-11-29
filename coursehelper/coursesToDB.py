import os
import json
import re
import database

def putCoursesToDB():
	current = os.path.dirname(os.path.abspath(__file__))
	parent = os.path.abspath(os.path.join(current, os.pardir))
	path = parent + "/courseCrawler/courses.txt"

	dontInclude = re.compile(r'/[a-zA-Z]\d\\')

	with open(path, 'r') as coursesTxt:
		for line in coursesTxt:
			courseJSON = json.loads(line)

			repeatingCourseFlag = re.search(r'[a-zA-Z]\d$', courseJSON['name'])

			if repeatingCourseFlag is None: # and courseJSON['active'] == '1':
				#print courseJSON['name']
				#print courseJSON
				print "Seeding the database!!!!"

				db = database.get_db()
				db.execute('INSERT INTO courses (courseid, description) VALUES (?, ?)', [courseJSON['name'] , str(courseJSON)])
	        	db.commit()