import os
import datetime
import sqlite3
import bcrypt
import flask

from coursehelper import app, ALLOWED_EXTENSIONS
from database import get_db, query_db
from sqlite3 import IntegrityError, Row
from werkzeug.utils import secure_filename

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def getFolderNameHash(title):
	return str(hash(title))


def uploadFilesAttempt(request, session):
	uploaded = flask.request.files.getlist('file[]')
	courseid = request.form['courseid']

	for aFile in uploaded:
		if aFile.filename == '':
			return False
		if not aFile or not allowed_file(aFile.filename):
			return False
		#if os.path.getsize(aFile) > app.config['MAX_CONTENT_LENGTH']:
			#return False

	title = request.form['title']
	folderNameHash = getFolderNameHash(title)
	uploadFolder = os.path.join((app.config['UPLOAD_FOLDER'] + '/' +  courseid + '/'), folderNameHash)

	#print "HASH : " + folderNameHash
	print "Upload folder would be: " +  uploadFolder
	print str(uploaded)

	for aFile in uploaded:
		filename = secure_filename(aFile.filename)
		print aFile

		try:
			path = os.path.join(uploadFolder , filename)
			written = writeFileLinkToDatabase(request, session, path)

			print "Written is: " + str(written)
			print path
			print "lel"
			print aFile

			print "I want to write " + str(aFile) + " to path: " + str(path)
			if written:
				print "SO CLOSE"
				print "I want to write " + str(aFile) + " to path: " + str(path)
				
				if not os.path.exists(uploadFolder):
    					os.makedirs(uploadFolder)

				aFile.save(path)
			
		except RequestEntityTooLarge:
			error = "File size can not be larger than 10 MB!"

	return True

def writeFileLinkToDatabase(request, session, path):
	username = session['username']
	courseid = request.form['courseid']
	title = request.form['title']
	url = path
	desc = request.form['desc']
	timestamp = datetime.datetime.now()

	db = get_db()

	try:
		if desc:
			db.execute('INSERT INTO resources (userid, courseid, title, url, description, tstamp) VALUES (?, ?, ?, ?, ?, ?)', [username, courseid, title, url, desc, timestamp])
			db.commit()
		else:
			db.execute('INSERT INTO resources (userid, courseid, title, url, tstamp) VALUES (?, ?, ?, ?, ?)', [username, courseid, title, url, timestamp])
			db.commit()
	except IntegrityError:
		db.rollback()
		error = "Invalid Entry!"
		print error
		return False

	return True

	




