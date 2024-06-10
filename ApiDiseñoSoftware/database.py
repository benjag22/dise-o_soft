from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database:
    def __init__(self):
        self.create_all()

    def create_all(self):
        db.create_all()