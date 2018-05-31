from flask import Blueprint
from flask import render_template, url_for, jsonify
from flask_restful import reqparse
from flask_login import login_user, logout_user

from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    args = parser.parse_args()
    email = args['email']
    user = User.get_by_email(email)
    data = dict(
        code=203,
        message="邮箱或密码错误!"
    )
    if user:
        password = args['password']
        if user.verify_password(password):
            login_user(user, True)
            data = dict(
                code=200,
                message="OK"
            )
    return jsonify(data)


@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    data = dict(
        code=200,
        message="OK"
    )
    return jsonify(data)
