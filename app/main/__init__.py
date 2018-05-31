from datetime import datetime
import time

from flask import Blueprint
from flask import render_template
from flask_login import current_user

from app import mail


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    return render_template(
        'home.html',
        update_count=5,
        current_user=current_user,
        date_time=time.strftime('%Y年%m月%d日 %H时%M分', now.timetuple())
    )