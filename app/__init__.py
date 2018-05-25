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

from app.main.forms.login import LoginForm
from app.utils.email import Mail


basedir = os.path.abspath(os.path.dirname(__file__)) 

app = Flask("Blog", static_folder='blog/static', template_folder='blog/templates')

app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

app.config['MAIL_HOSTNAME'] = 'smtp.bigbin.club'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'bigbin@bigbin.club'
app.config['MAIL_PASSWORD'] = 'BINbin13078313586'
app.config['MAIL_SENDER'] = "Mr.Lean <bigbin@bigbin.club>"

login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
mail = Mail(app)


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