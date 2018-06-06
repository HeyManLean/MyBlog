from flask_restful import reqparse, Resource
from flask_login import login_user, logout_user
from flask import make_response, jsonify

from app.models import User


class SessionResource(Resource):
    def get(self):
        return {}

    def post(self):
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
