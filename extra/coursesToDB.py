import os
import json
import re

def main():
	current = os.path.dirname(os.path.abspath(__file__))
	parent = os.path.abspath(os.path.join(current, os.pardir))
	path = parent + "/courseCrawler/courses.txt"

	dontInclude = re.compile(r'/[a-zA-Z]\d\\')

	coursesTxt = open(path, 'r')
	for i in range(500):
		line = coursesTxt.readline()
		courseJSON = json.loads(line)

		repeatingCourseFlag = re.search(r'[a-zA-Z]\d$', courseJSON['name'])

		if repeatingCourseFlag is None and courseJSON['active'] == '1':
			print courseJSON['name'] + " - " + courseJSON['active']

main()