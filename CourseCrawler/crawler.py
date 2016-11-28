import os
import urllib2
import json

from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from xml.dom.minidom import parseString

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

def jsonifyCourse(link):
	course = {}
	#print 'link : ' + link
	course['link'] = link
	soup = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')
	info = soup.find("div", {"id": "main-column"})
	#finder = CourseInfoFinder()
		
	title = soup.find_all("h1")[0]
	doc = parseString(str(title))
	doc = parseString(str(info))
	paragraph = doc.getElementsByTagName("p")
	a = doc.getElementsByTagName("a")
	
	#print 'name : ' + (str(title).split('>')[1]).split('<')[0].strip()
	name = (str(title).split('>')[1]).split('<')[0].strip()
	course['name'] = name.encode("utf-8")

	for i in range(len(paragraph)):
		if i == 0:
			faculty = a[0].firstChild.data
			#print 'faculty : ' + faculty
			course['faculty'] = faculty.encode("utf-8")
		elif i == 1:
			description = paragraph[i].firstChild.data.strip()
			#print 'description : ' + description
			course['description'] = description.encode("utf-8")
		elif i == 2:
			terms = paragraph[i].firstChild.data.split(':')[1].strip()
			if terms.startswith('This'):
				#print 'offered : false'
				course['offered'] = "false"
			else:
				#print 'oferred : true'
				course['offered'] = "true"
			#print 'terms : ' + terms
			course['terms'] = terms.encode("utf-8")
		elif i == 3:
			instructors = paragraph[i].firstChild.data.split(':')[1].strip()
			#print 'instructors : ' + instructors
			course['instructors'] = instructors.encode("utf-8")
		elif i == 4:
			#Not considering the 'and' 'or' keywords in prereqs descriptions with this code
			if paragraph[i].firstChild.data.startswith('Pre'):
				prereqs = []
				for j in range(1, len(a)):
					prereqs.append(a[j].firstChild.data)
				#print 'prereqs : ' + ', '.join(prereqs)
				course['prereqs'] = ', '.join(prereqs).encode("utf-8")
				#print 'restrictions : null'
				course['restrictions'] = "null"
			else:
				#print 'prereqs : null'
				course['prereqs'] = "null"
				#print 'restrictions : ' + paragraph[i].firstChild.data.split(':')[1].strip()
				course['restrictions'] = paragraph[i].firstChild.data.split(':')[1].strip().encode("utf-8")
		elif i == 5:
			#print 'notes : ' + paragraph[i].firstChild.data
			course['notes'] = paragraph[i].firstChild.data.encode("utf-8")
	if len(paragraph) < 6:
		#print 'notes : null'
		course['notes'] = "null"
	#print '\n\n'
	return course

# def getXMLTree(soup, tag):
# 	doc = parseString(str(soup))
# 	tree = doc.getElementsByTagName(tag)
# 	return tree

# def getElementsList(tree):
# 	elements = []
# 	for j in range(len(tree)):
# 		elements.append(tree[j].firstChild.data.encode("utf-8"))
# 	return elements

# def getInfoByClass(soup, div, className, searchedTag):
# 	info = soup.find_all(div, class_=className)[0]
# 	foundText = getElementsList(getXMLTree(info, searchedTag))
# 	print foundText

# def getInfoByID(soup, div, className, searchedTag):
# 	info = soup.find_all(div, id=className)[0]
# 	foundText = getElementsList(getXMLTree(info, searchedTag))
# 	print foundText

# def getMeta(soup):
# 	getInfoByClass(soup, "div", "meta", 'p')
# 	getInfoByClass(soup, "div", "meta", 'a')

# def getContent(soup):
# 	getInfoByID(soup, "div", 'main-column', 'p')

# def getContentByClass(soup, div, className, tag):
# 	content = [info.find(tag) for info in soup.find_all(div, class_=className)]
# 	for i in range(len(content)):
# 		print content[i]

# def getContentByID(soup, div, id, idValue, tag):
# 	content = [info.find_all(tag) for info in soup.find_all(div, {id : idValue})]
# 	return content[0]

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

def addTitle(dict, soup):
	dict['title'] = (formatContent(getInnerContentSection(soup, 'h1', ''))[0].strip())

def addMeta(dict, soup):
	string = ""
	infoList = formatContent(getInnerContentSection(soup, 'div', 'meta'))
	for field in infoList:
		string = string + field.replace("amp;", "&")
		if field == ')':
			string = string + " "
	#dict['meta'] = string.strip()
	dict['faculty'] = string.split(":")[1].strip()

def addTerms(dict, soup):
	dict['terms'] = formatContent(getInnerContentSection(soup, 'p', 'catalog-terms'))[0].split(":")[1].strip()
def addInstructors(dict, soup):
	dict['instructors'] = formatContent(getInnerContentSection(soup, 'p', 'catalog-instructors'))[0].split(":")[1].strip()

# def addNotes(dict, soup):
# 	string = ""
# 	infoList = formatContent(getInnerContentSection(soup, 'ul', 'catalog-notes'))[0]
# 	#infoList = infoList[0].find_all
# 	infoDict = {}
# 	for field in infoList:
# 		string = string + field.replace("amp;", "&")
# 		if field == ')':
# 			string = string + " "
# 	dict['notes'] = string.strip()
# 	#print infoList

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

def main():
	f = open('courses', 'w')
	idNum = 1;

	for pageNum in range(506):
		soup = BeautifulSoup(urllib2.urlopen('http://www.mcgill.ca/study/2016-2017/courses/search?search_api_views_fulltext=&sort_by=field_subject_code&page=' + str(pageNum)).read(), 'html.parser')
		eCalendar = soup.find_all("div", class_="view-content")

		parser = CourseLinkFinder("http://www.mcgill.ca")

		parser.feed(str(eCalendar))
		for i in range(len(parser.links)):
			#course = jsonifyCourse(parser.links[i])
			#print json.dumps(course, sort_keys=True)
			link = parser.links[i]
			#print "Link : " + str(link)
			print "Link = " + link + '\n'
			soup = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')

			courseJSON = {}

			addTitle(courseJSON, soup)
			addMeta(courseJSON, soup)
			addTerms(courseJSON, soup)
			addInstructors(courseJSON, soup)
			addNotes(courseJSON, soup)
			addDescription(courseJSON, soup)
			courseJSON['link'] = link
			courseJSON['id'] = str(idNum)

			#courses = [info.find_all('div', class_='content') for info in soup.find_all('div', {'id' : 'inner-container'})]
			#overview = courses[0][0].find_all('p')
			#print str(overview[1]) + '\n\n'
			#courses = courses[0][0].findAll('div', {'class': 'content'})
			#courses = courses[0].findAll('p')
			#print courses
			JSONToWrite = json.dumps(courseJSON, sort_keys=True)
			print JSONToWrite
			print '\n'
			#print json.dumps(courseJSON, sort_keys=True)
			#content = [info.find_all('ul', class_='catalog-notes') for info in soup.find_all('div', {'id' : 'inner-container'})]
			#c2 = [info for info in content]
			#print c2[0][0].find_all('li')
			f.write(JSONToWrite)
			f.write('\n')
			idNum = idNum + 1
	f.close()
			

main()