from flask_restful import Resource
from flask_login import login_user, logout_user
from flask import make_response, jsonify
from flask_restful.reqparse import Argument

from app.models import User
from app.api.utils import get_params


class SessionResource(Resource):
    def post(self):
        (email, password) = get_params([
            Argument('email', type=str, required=True),
            Argument('password', type=str, required=True)
        ])
        user = User.get_by_email(email)
        data = dict(
            code=203,
            message="邮箱或密码错误!"
        )
        if user and user.verify_password(password):
            login_user(user, True)
            data = dict(
                code=200,
                message="OK"
            )
        response = make_response(jsonify(data))
        response.set_cookie('nickname', user.nickname)
        return response

    def delete(self):
        logout_user()
        data = dict(
            code=200,
            message="OK"
        )
        response = make_response(jsonify(data))
        response.set_cookie('nickname', '', expires=0)
        return response
