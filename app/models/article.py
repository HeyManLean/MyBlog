from datetime import datetime
from enum import Enum

from app import db, parser


class ArticleStatus:
    DELETED = 0
    NORMAL = 1


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text)
    html = db.Column(db.Text)
    abscontent = db.Column(db.Text)
    user_id = db.Column(db.SmallInteger, db.ForeignKey('user.id'))

    status = db.Column(db.SmallInteger, default=ArticleStatus.NORMAL)

    published_id = db.Column(db.Integer, db.ForeignKey('published_article.id'))
    published_article = db.relationship('PublishedArticle')

    category_id = db.Column(db.Integer, db.ForeignKey(
        'article_category.id'), nullable=False)
    category = db.relationship('ArticleCategory')

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Article %d>' % self.id

    @classmethod
    def insert(cls, user_id, title, category_id, content=None):
        new_article = Article()
        new_article.title = title
        new_article.category_id = category_id
        new_article.content = content
        new_article.user_id = user_id
        if content:
            new_article.abscontent = parser.get_abscontent(html)
        db.session.add(new_article)
        db.session.flush()
        return new_article

    def update(self, title, content, html, category_id):
        self.title = title
        self.content = content
        self.html = html
        if category_id:
            self.category_id = category_id
        if content:
            self.abscontent = parser.get_abscontent(html)
        db.session.flush()
        return True

    @classmethod
    def get_by_userid(cls, user_id):
        return cls.query.filter_by(
            user_id=user_id
        ).all()
    
    @classmethod
    def get_by_categoryid(cls, category_id):
        return cls.query.filter_by(
            category_id=category_id,
            status=ArticleStatus.NORMAL).all()


class PublishedArticle(db.Model):
    __tablename__ = 'published_article'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    html = db.Column(db.Text)
    abscontent = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=ArticleStatus.NORMAL)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'article_category.id'), nullable=False)
    category = db.relationship('ArticleCategory')

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


class Subject(Enum):
    Programming = "编程语言"
    ComputerTheory = "计算机原理"
    Web = "WEB开发"
    Other = "其他"
    


class ArticleCategory(db.Model):
    __tablename__ = 'article_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    css = db.Column(db.String(64), nullable=False,
                    default="glyphicon glyphicon-leaf")
    subject = db.Column(db.String(32), nullable=False,
                        default=Subject.Programming.value)

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<ArticleCategory %s>' % self.name

    @classmethod
    def get_by_subject(cls, subject):
        return cls.query.filter_by(
            subject=subject
        ).all()

    @classmethod
    def insert(cls, name):
        new_category = cls()
        new_category.name = name
        db.session.add(new_category)
        db.session.flush()
        return new_category
