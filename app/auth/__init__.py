from flask import Blueprint
from flask import render_template, url_for


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    return render_template('home.html')


@auth.route('/logout')
def logout():
    return render_template('home.html')