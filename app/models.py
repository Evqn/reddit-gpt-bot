from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # bot settings
    reddit_user = db.Column(db.String(1000))
    max_sentence = db.Column(db.String(1000))
    tone = db.Column(db.String(1000))
    additional = db.Column(db.String(1000))
