from flask_restful import reqparse, Resource
from flask_login import login_required, current_user

from app.models import Article
from app import db


class ArticlesResource(Resource):
    @login_required
    def post(self):
        new_article = Article.insert(current_user.id)
        db.session.commit()
        data = dict(
            code=200,
            message="ok",
            id=new_article.id
        )
        return data


class ArticlesIdResource(Resource):
    def get(self, id):
        article = Article.query.get(id)
        if not article:
            data = dict(
                code=404,
                message="The requested article is not found"
            )
        else:
            data = dict(
                code=200,
                message="ok",
                title=article.title,
                html=article.html,
                content=article.content,
                username=article.user.nickname,
                create_time=article.create_time
            )
        return data

    @login_required
    def put(self, id):
        article = Article.query.get(id)
        if not article:
            data = dict(
                code=404,
                message="The requested article is not found"
            )
        else:
            parser = reqparser.RequestParser()
            parser.add_argument('title', type=str, required=True)
            parser.add_argument('content', type=str, required=True)
            args = parser.parse_args()

            title = args['title']
            content = args['content']
            html = args['html']

            Article.update(title, content, html)
            data = dict(
                code=200,
                message="ok"
            )
        return data
