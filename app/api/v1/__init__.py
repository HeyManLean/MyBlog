from flask_restful import Api

from app.api import api
from .article import ArticlesResource, ArticlesIdResource, ArticleCategoriesResource, ArticlePublishResource
from .file import FileResource

api_v1 = Api(api, prefix='/v1')


api_v1.add_resource(ArticlesResource, '/articles')
api_v1.add_resource(ArticlesIdResource, '/articles/<int:id>')
api_v1.add_resource(ArticlePublishResource, '/articles/<int:id>/publish')
api_v1.add_resource(ArticleCategoriesResource, '/article_categories')
api_v1.add_resource(FileResource, '/upload')
