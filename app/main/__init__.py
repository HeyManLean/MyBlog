from datetime import datetime
import time

from flask import Blueprint
from flask import render_template, request, redirect
from flask_login import current_user, login_user
from sqlalchemy import extract

from app import db
from app.models import PublishedArticle, ArticleCategory, ArticleStatus, User


main = Blueprint('main', __name__)


@main.route('/')
def index():
    articles = PublishedArticle.query.filter_by(
        status=ArticleStatus.NORMAL).all()
    return render_template('base.html', articles=articles, location="home")


@main.route('/about')
def about():
    return render_template('base.html', location="about")


@main.route('/categories')
def categories():
    article_categories = ArticleCategory.get_valid_categories()
    categories = []

    for a_category in article_categories:
        articles = PublishedArticle.query.filter_by(
            category_id=a_category.id,
            status=ArticleStatus.NORMAL
        ).all()
        if articles:
            categories.append(
                dict(
                    name=a_category.name,
                    posts=articles
                )
            )
    return render_template('base.html', categories=categories, location="categories")


@main.route('/archives')
def archives():
    years = db.session.query(
        extract('year', PublishedArticle.create_time)).distinct().all()
    archives = []
    for year in years:
        articles = PublishedArticle.query.filter(
            extract('year', PublishedArticle.create_time) == year[0],
            PublishedArticle.status == ArticleStatus.NORMAL
        ).all()
        archives.append(
            dict(
                date=year[0],
                posts=articles
            )
        )
    return render_template('base.html', archives=archives, location="archives")


@main.route('/posts/<int:id>')
def post(id):
    post = PublishedArticle.query.filter_by(
        id=id,
        status=ArticleStatus.NORMAL
    ).first()
    if not post:
        return redirect('/')
    return render_template('base.html', post=post, location="posts")


@main.route('/editor')
def editor():
    if not current_user.is_active:
        return redirect('/login')
    return render_template('editor.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # email = request.form['email']
        password = request.form['password']
        user = User.get_by_email("565743040@qq.com")
        if user:
            if user.verify_password(password):
                login_user(user)
                return redirect('/editor')
    return render_template('login.html')
