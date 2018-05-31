from datetime import datetime
import time

from flask import Blueprint
from flask import render_template
from flask_login import current_user

from app.main.forms.login import LoginForm
from app import mail


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        mail.send_mail(login_form.email.data)
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