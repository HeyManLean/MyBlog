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
    return render_template('index.html', articles=articles, dtimeformat=dtimeformat)


@main.route('/about')
def about():
    return render_template('about.html')


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
    return render_template('category.html', categories=categories, dtimeformat=dtimeformat)


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
    return render_template('archive.html', archives=archives, dtimeformat=dtimeformat)
