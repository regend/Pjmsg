from flask import app, Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'Regend'

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
