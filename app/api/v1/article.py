from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask_login import login_required, current_user

from app import db
from app.api.utils import get_params
from app.models import Article, ArticleCategory, PublishedArticle, Subject
from app.utils.data import date2stamp


class ArticlesResource(Resource):
    @login_required
    def get(self):
        articles = current_user.articles
        articles_data = [
            dict(
                id=a.id,
                title=a.title,
                html=a.abscontent,
                author=a.user.nickname,
                create_time=date2stamp(a.create_time),
                view_count=0)
            for a in articles]
        data = dict(
            list=articles_data,
            code=200,
            message="ok"
        )
        return data

    @login_required
    def post(self):
        (title, category_id) = get_params([
            Argument('title', type=str, required=True),
            Argument('category_id', type=int, required=True)
        ])
        new_article = Article.insert(
            current_user.id,
            title,
            category_id
        )
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
                category_id=article.category_id,
                content=article.content,
                author=article.user.nickname,
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
            (title, content, html, category_id) = get_params([
                Argument('title', type=str, required=True),
                Argument('content', type=str, required=True),
                Argument('html', type=str, required=True),
                Argument('category_id', type=int)
            ])
            article.update(title, content, html, category_id)
            db.session.commit()
            data = dict(
                code=200,
                message="ok"
            )
        return data

    @login_required
    def delete(self, id):
        article = Article.query.get(id)
        if not article:
            data = dict(
                code=404,
                message="The requested article is not found"
            )
        else:
            db.session.delete(article)
            db.session.commit()
            data = dict(
                code=200,
                message="ok"
            )
        return data


class ArticleCategoriesResource(Resource):
    def get(self):
        categories_data = []
        for item in Subject:
            subject_name = item.value
            categories = ArticleCategory.get_by_subject(subject_name)
            if categories:
                categories_data.append(dict(
                    subject=subject_name,
                    categories=[dict(
                        id=c.id,
                        name=c.name,
                        css=c.css
                    ) for c in categories]
                ))
        return dict(
            list=categories_data,
            code=200,
            message="ok"
        )

