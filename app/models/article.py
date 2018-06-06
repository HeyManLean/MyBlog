from datetime import datetime

from app import db


class ArticleStatus:
    DELETED = 0
    NORMAL = 1


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)
    html = db.Column(db.Text)
    user_id = db.Column(db.SmallInteger, db.ForeignKey('user.id'))
    status = db.Column(db.SmallInteger, default=ArticleStatus.NORMAL, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Article %d>' % self.id
    
    @classmethod
    def insert(cls, user_id, title='Untitled', content=None):
        new_article = Article()
        new_article.title = title
        new_article.content = content
        new_article.user_id = user_id
        db.session.add(new_article)
        db.session.flush()
        return new_article

    def update(self, title, content, html):
        self.title = title
        self.content = content
        self.html = html
        db.session.flush()
        return True