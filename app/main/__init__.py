from datetime import datetime
import time

from flask import Blueprint
from flask import render_template
from flask_login import current_user
from sqlalchemy import extract

from app import db
from app.models import Article, ArticleCategory
from app.utils.data import dtimeformat


main = Blueprint('main', __name__)


@main.route('/')
def index():
    articles = Article.query.all()
    return render_template('base.html', articles=articles, dtimeformat=dtimeformat, location="home")


@main.route('/about')
def about():
    return render_template('base.html', location="about")


@main.route('/categories')
def categories():
    article_categories = ArticleCategory.query.all()
    categories = []

    for a_category in article_categories:
        articles = Article.query.filter_by(category_id=a_category.id).all()
        categories.append(
            dict(
                name=a_category.name,
                posts=articles
            )
        )
    return render_template('base.html', categories=categories, dtimeformat=dtimeformat, location="categories")


@main.route('/archives')
def archives():
    years = db.session.query(
        extract('year', Article.create_time)).distinct().all()
    archives = []
    for year in years:
        articles = Article.query.filter(
            extract('year', Article.create_time) == year[0]).all()
        archives.append(
            dict(
                date=year[0],
                posts=articles
            )
        )
    return render_template('base.html', archives=archives, dtimeformat=dtimeformat, location="archives")


@main.route('/posts/<int:id>')
def post(id):
    post = Article.query.get(id)
    return render_template('base.html', post=post, location="posts", dtimeformat=dtimeformat)
