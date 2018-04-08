from flask import Flask, redirect
from flask_login import current_user, LoginManager


login_manager = LoginManager()


def create_app():
    blog_app = Flask("Blog")
    login_manager.init_app(blog_app)
    return blog_app


app = create_app()


@app.before_request
def check_is_login():
    if not current_user.is_active:
        return "ok"
