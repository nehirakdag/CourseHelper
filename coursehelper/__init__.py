import os

from flask import Flask, Request, render_template, request, session, g, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, './db/courseHelper.db'),
    SECRET_KEY='749qeBLYQpm633ZR+1WKQnuabvDPXgsd',
    USERNAME='admin',
    PASSWORD='default'
))

import coursehelper.views
import coursehelper.coursesToDB

# with app.app_context():
    # coursesToDB.putCoursesToDB()
#app.config.from_envvar('COURSEHELPER_SETTINGS', silent=True)

