from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True, index=True)
    nickname = db.Column(db.String(16))
    password = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    articles = db.relationship('Article', backref='user', order_by='Article.id')

    def __repr__(self):
        return '<User %r>' % self.nickname