import datetime
import sqlite3
import collections

from coursehelper import app, ALLOWED_EXTENSIONS
from database import get_db, query_db
from sqlite3 import IntegrityError, Row

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


