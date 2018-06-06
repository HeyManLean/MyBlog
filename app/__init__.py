from flask import Flask
from flask import request
from flask import render_template
from flask_login import current_user
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from app.utils.email import Mail
from config import config


login_manager = LoginManager()
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name='testing'):
    app = Flask("Blog", static_folder='app/static', template_folder='app/templates')
    app.config.from_object(config[config_name])
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)

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
                request.url))
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.api import api
    app.register_blueprint(api)
    return app
