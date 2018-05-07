from flask import Flask, request, render_template
from flask_login import current_user, LoginManager


login_manager = LoginManager()


def create_app():
    blog_app = Flask("Blog", static_folder='blog/static', template_folder='blog/templates')
    login_manager.init_app(blog_app)
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
    return render_template('index.html')