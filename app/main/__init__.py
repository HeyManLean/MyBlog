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
    now = datetime.now()
    return render_template(
        'home.html'
    )


@main.route('/articles/<int:id>/read')
def articles_read(id):
    return render_template("show.html")


@main.route('/articles/<int:id>/write')
def articles_write(id):
    return render_template('editor.html')


@main.route('/my-articles')
def my_articles():
    articles = Article.get_by_userid(current_user.id)
    return render_template("list.html", current_user=current_user, articles=articles)
