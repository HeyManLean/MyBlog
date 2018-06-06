from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask_login import login_required, current_user

from app import db
from app.api.utils import get_params
from app.models import Article
from app.utils.data import date2stamp


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
                create_time=date2stamp(article.create_time)
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
            (title, content, html) = get_params([
                Argument('title', type=str, required=True),
                Argument('content', type=str, required=True),
                Argument('html', type=str, required=True)
            ])
            article.update(title, content, html)
            db.session.commit()
            data = dict(
                code=200,
                message="ok"
            )
        return data
