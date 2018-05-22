from datetime import datetime
import time
import os

from flask import Flask
from flask import request
from flask import render_template
from flask import g
from flask_login import current_user
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from blog.forms.login import LoginForm


login_manager = LoginManager()
bootstrap = Bootstrap()
csrf = CSRFProtect()
db = SQLAlchemy()


basedir = os.path.abspath(os.path.dirname(__file__)) 


def create_app():
    blog_app = Flask("Blog", static_folder='blog/static', template_folder='blog/templates')
    login_manager.init_app(blog_app)
    bootstrap.init_app(blog_app)
    csrf.init_app(blog_app)
    db.init_app(blog_app)

    blog_app.config['SECRET_KEY'] = 'SECRET_KEY'
    blog_app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    blog_app.config['SQLCHEMY_COMMIT_ON_TEARDOWN'] = True
    blog_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    blog_app.config['DEBUG'] = True
    return blog_app


app = create_app()


@app.before_request
def before_request():
    print(
        "====================================================================================================\n"
        "客户端: {0}\n"
        "登录状态: {1}\n"
        "Ip地址: {2}\n"
        "端口: {3}\n"
        "Cookies: {4}\n"
        "Url: {5}\n"
        "====================================================================================================\n"
        .format(
            request.headers.get('User-Agent'),
            "已登录" if current_user.is_active else "未登录",
            request.remote_addr,
            request.environ['REMOTE_PORT'],
            request.cookies,
            request.url
        )
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(login_form.email.data, login_form.password.data)
        print('request correct!')
    else:
        print('request invalid!')
    return render_template(
        'home.html', 
        p_names=["python", "Javascript", "C++"],
        update_count=5,
        username=current_user.username if current_user.is_active else None,
        date_time=time.strftime('%Y年%m月%d日 %H时%M分', now.timetuple()),
        login_form=login_form
    )