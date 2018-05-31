from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True, index=True)
    nickname = db.Column(db.String(16))
    __password = db.Column('password', db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    articles = db.relationship('Article', backref='user', order_by='Article.id')

    def __repr__(self):
        return '<User %r>' % self.nickname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.__password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.__password, password)