from flask_restful import Api

from app.api import api
from .session import SessionResource
from .article import ArticlesResource, ArticlesIdResource

api_v1 = Api(api, prefix='/v1')


api_v1.add_resource(SessionResource, '/session')
api_v1.add_resource(ArticlesResource, '/articles')
api_v1.add_resource(ArticlesIdResource, '/articles/<int:id>')
