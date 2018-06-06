from flask import Blueprint


api = Blueprint('api', __name__, url_prefix='/api')


from .v1 import api_v1