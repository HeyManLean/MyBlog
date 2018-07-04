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
    return render_template(
        'index.html'
    )
