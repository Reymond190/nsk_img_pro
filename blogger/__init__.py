from flask import Flask

app = Flask(__name__)
app.secret_key = 'hello_world'
app.config.from_object(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ray.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024         # max file size

from blogger import models
from blogger import views

