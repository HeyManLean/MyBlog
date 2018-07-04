from datetime import datetime
import time

from flask import Blueprint
from flask import render_template
from flask_login import current_user

from app import mail
from app.models import Article


main = Blueprint('main', __name__)


@main.route('/')
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/categories')
def categories():
    return render_template('category.html')


@main.route('/archives')
def archives():
    return render_template('archive.html')