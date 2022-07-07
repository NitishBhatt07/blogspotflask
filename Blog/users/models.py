
from Blog import db
from datetime import datetime
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    profile_pic = db.Column(db.String(500), nullable=True)
    cover_pic = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(500), nullable=False)
    registered_on = db.Column(db.DateTime(), default=datetime.utcnow())

    # one to many {user have multiple posts}
    posts = db.relationship('Posts', backref='poster')

    def __repr__(self):
        return '<Username %r>' % self.username
