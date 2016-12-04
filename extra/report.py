import os
import re
import yaml
import json

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

def main():
	current = os.path.dirname(os.path.abspath(__file__))
	parent = os.path.abspath(os.path.join(current, os.pardir))
	path = parent + "/courseCrawler/courses.txt"

	i = 0

	with open(path, 'r') as coursesTxt:
		for line in coursesTxt:
			#courseJSON = yaml.safe_load(line)
			if i == 0:
				print yaml.safe_load(line)
				print json.loads(line)

			if is_json(line):
				courseJSON = yaml.safe_load(line)
				#print "Course " + courseJSON['title'] + " is okay"
			else:
				print "Noooooo"
			i = i + 1

	print "Num = " + str(i)



main()