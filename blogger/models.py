from flask_sqlalchemy import SQLAlchemy
import datetime
from blogger import app

db = SQLAlchemy(app)

class temp_file_names(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temp_id = db.Column(db.String(100),nullable=True)
    user_id = db.Column(db.String(100),nullable=True)
    temp_file_type = db.Column(db.String(100),nullable=True)
    temp_file_name = db.Column(db.String(1000),nullable=True)
    status = db.Column(db.String(1000),default='saved')         # ['saved','cleaned']

    def __init__(self, temp_id, user_id,temp_file_type, temp_file_name,status):
        self.temp_id = temp_id
        self.user_id = user_id
        self.temp_file_type = temp_file_type
        self.temp_file_name = temp_file_name
        self.status = status

db.create_all()