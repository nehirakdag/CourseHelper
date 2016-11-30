import os
import re
import database
import yaml

def putCoursesToDB():
	current = os.path.dirname(os.path.abspath(__file__))
	parent = os.path.abspath(os.path.join(current, os.pardir))
	path = parent + "/courseCrawler/courses.txt"

	uploads = current + "/uploads/"

	#dontInclude = re.compile(r'[a-zA-Z]\d\\')
	previous = ""
	print "Seeding the database!!!!"
	i = 0

	with open(path, 'r') as coursesTxt:
		for line in coursesTxt:
			courseJSON = yaml.safe_load(line)

			repeatingCourseFlag = re.search(r'[a-zA-Z]\d$', courseJSON['name'])

			if repeatingCourseFlag is None or courseJSON['name'][:7] != previous[:7]: # and courseJSON['active'] == '1':
				keyToStore = courseJSON['name']
				
				if len(courseJSON['name']) > 7:
					if not repeatingCourseFlag is None: #courseJSON['name'].endswith(r'[a-zA-Z]\d'):
						keyToStore = courseJSON['name'][:-2]
						#if keyToStore[:-2] != previous[:-2]:
							#print courseJSON['name']
				
				#if keyToStore.startswith("FI"):
				#		print keyToStore			

				if len(keyToStore) > 7:
					m = re.search(r'\d{1}$', keyToStore)
					if m is not None:
						keyToStore = keyToStore[:-2]
					#print "Infidel : " + keyToStore
				
				if keyToStore != previous:
					i = i + 1
					#print str(courseJSON).decode('utf-8')
					print str(courseJSON).replace('\'', '"')
					db = database.get_db()
					db.execute('INSERT INTO courses (courseid, description) VALUES (?, ?)', [keyToStore , str(courseJSON).replace('\'', '"')])
	        		db.commit()

	        		uploadFolder = uploads + keyToStore
	        		if not os.path.exists(uploadFolder):
    					os.makedirs(uploadFolder)

	        	previous = keyToStore
		print str(i)
