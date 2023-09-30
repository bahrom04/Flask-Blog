from flask import Flask,render_template
import os
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

app.config['UPLOAD_FOLDER'] = 'webapp/' + UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bahromoken@githubbahrombek'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/blog'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from webapp import routes



