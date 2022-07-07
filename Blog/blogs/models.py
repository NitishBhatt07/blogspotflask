from Blog import db
from datetime import datetime

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    post_pic = db.Column(db.String(500), nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow())

    # Foreign Key to link Users (refer to PK of Users)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Title %r>'% self.title
