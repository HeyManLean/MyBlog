from flask import Flask
from flask import request
from flask import render_template
from flask import g
from flask_login import current_user
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
    blog_app = Flask("Blog", static_folder='blog/static', template_folder='blog/templates')
    login_manager.init_app(blog_app)
    bootstrap.init_app(blog_app)
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


@app.route('/')
def index():
    return render_template(
        'home.html', 
        p_names=["python", "Javascript", "C++"],
        update_count=5,
        username='hello'#current_user.username if current_user.is_active else None
    )