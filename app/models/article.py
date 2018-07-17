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
    user_id = db.Column(db.SmallInteger, db.ForeignKey('user.id'))

    status = db.Column(db.SmallInteger, default=ArticleStatus.NORMAL, nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)

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
    status = db.Column(db.SmallInteger, default=ArticleStatus.NORMAL, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'article_category.id'), nullable=False)
    category = db.relationship('ArticleCategory')

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)


class CategoryStatus:
    DELETED = 0
    NORMAL = 1


class ArticleCategory(db.Model):
    __tablename__ = 'article_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    status = db.Column(db.SmallInteger, default=CategoryStatus.NORMAL)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<ArticleCategory %s>' % self.name

    @classmethod
    def insert(cls, name):
        new_category = cls()
        new_category.name = name
        db.session.add(new_category)
        db.session.flush()
        return new_category

    @classmethod
    def delete(cls, id):
        category = cls.query.get(id)
        if category:
            articles = Article.get_by_categoryid(id)
            for a in articles:
                a.status = ArticleStatus.DELETED
            category.status = CategoryStatus.DELETED
            db.session.flush()
        return True

    @classmethod
    def rename(cls, id, new_name):
        category = cls.query.get(id)
        if category.name != new_name:
            category.name = new_name
            db.session.flush()
        return True

    @classmethod
    def get_valid_categories(cls):
        return cls.query.filter_by(status=CategoryStatus.NORMAL).all()
