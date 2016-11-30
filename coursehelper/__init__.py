import os

from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

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

