import os
import urllib2
import json

from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

class CourseLinkFinder(HTMLParser):
	def __init__(self, base_url):
		HTMLParser.__init__(self)
		self.base_url = base_url
		self.links = []

	def error(self, message):
		pass

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for (attribute, value) in attrs:
				if attribute == 'href':
					link = self.base_url + value
					#print link
					self.links.append(link)


class CourseInfoFinder(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.courseInfo = []
		self.listening = 0

	def error(self, message):
		pass

	def handle_starttag(self, tag, attrs):
		if tag == 'p' or tag == 'h1':
			self.listening += 1

	def handle_endtag(self, tag):
		if tag == 'p' or tag == 'h1' and self.listening:
			self.listening -= 1

	def handle_data(self, data):
		if self.listening:
			self.courseInfo.append(data)
			#print data

def formatContent(content):
	if len(content) > 0:
		formatter = CourseInfoFinder()
		formatter.feed(str(content[0]))
		course = formatter.courseInfo
		return course
	else:
		return ""

def formatLine(line):
	formatter = CourseInfoFinder()
	formatter.feed(str(line))
	course = " ".join(formatter.courseInfo)
	return course

def addToDict(dict, key, value):
	dict[key] = value

def getInnerContentSection(soup, tag, className):
	content = [info.find_all(tag, class_=className) for info in soup.find_all('div', {'id' : 'inner-container'})]
	return content[0]

def getInnerContentList(soup, tag, className):
	content = [info.find_all(tag, class_=className) for info in soup.find_all('div', {'id' : 'inner-container'})]
	return content

def addTitleAndName(dict, soup):
	title = (formatContent(getInnerContentSection(soup, 'h1', ''))[0].strip())
	dict['title'] = title

	name = title.split(" ")
	dict['name'] = name[0] + name[1]

def addMeta(dict, soup):
	string = ""
	infoList = formatContent(getInnerContentSection(soup, 'div', 'meta'))
	for field in infoList:
		string = string + field.replace("amp;", "&")
		if field == ')':
			string = string + " "
	dict['faculty'] = string.split(":")[1].strip()

def addTerms(dict, soup):
	terms = formatContent(getInnerContentSection(soup, 'p', 'catalog-terms'))[0].split(":")[1].strip()
	dict['terms'] = terms

	if terms.startswith("This"):
		dict['active'] = str(0)
	else:
		dict['active'] = str(1)

def addInstructors(dict, soup):
	dict['instructors'] = formatContent(getInnerContentSection(soup, 'p', 'catalog-instructors'))[0].split(":")[1].strip()

def addNotes(dict, soup):
	string = ""
	infoList = getInnerContentList(soup, 'ul', 'catalog-notes')[0]
	infoDict = {}
	infoDict['noteList'] = []

	if len(infoList) > 0:
		infoList = getInnerContentList(soup, 'ul', 'catalog-notes')[0][0].find_all('li')
		for item in infoList:
			infoDict['noteList'].append(formatLine(item))
	dict['notes'] = infoDict['noteList']

def addDescription(dict, soup):
	string = ""
	infoList = getInnerContentList(soup, 'div', 'content')[0]
	infoList = infoList[0].findAll('div', {'class': 'content'})
	infoList = infoList[0].findAll('p')
	dict['decription'] = formatLine(infoList[0]).strip()

def addCourse(dict, soup):
	addTitleAndName(dict, soup)
	addMeta(dict, soup)
	addTerms(dict, soup)
	addInstructors(dict, soup)
	addNotes(dict, soup)
	addDescription(dict, soup)

def main():
	f = open('courses2.txt', 'w')
	idNum = 1;

	for pageNum in range(506):
		soup = BeautifulSoup(urllib2.urlopen('http://www.mcgill.ca/study/2016-2017/courses/search?search_api_views_fulltext=&sort_by=field_subject_code&page=' + str(pageNum)).read(), 'html.parser')
		eCalendar = soup.find_all("div", class_="view-content")

		parser = CourseLinkFinder("http://www.mcgill.ca")
		parser.feed(str(eCalendar))

		for i in range(len(parser.links)):
			link = parser.links[i]

			print "Link = " + link + '\n'
			soup = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')

			courseJSON = {}

			addCourse(courseJSON, soup)
			courseJSON['link'] = link
			courseJSON['id'] = str(idNum)

			JSONToWrite = json.dumps(courseJSON, sort_keys=True)
			
			print JSONToWrite
			print '\n'
			
			f.write(JSONToWrite)
			f.write('\n')
			idNum = idNum + 1
	
	f.close()
			
main()