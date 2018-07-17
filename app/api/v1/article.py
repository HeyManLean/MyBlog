from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask_login import login_required, current_user

from app import db
from app.api.utils import get_params
from app.models import Article, ArticleCategory, PublishedArticle
from app.utils.data import date2stamp


class ArticlesResource(Resource):
    # @login_required
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

    # @login_required
    def post(self):
        (title, category_id) = get_params([
            Argument('title', type=str, required=True),
            Argument('category_id', type=int, required=True)
        ])
        new_article = Article.insert(
            # current_user.id,
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
                category_id=article.category_id,
                content=article.content,
                create_time=date2stamp(article.create_time)
            )
        return data

    # @login_required
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

    # @login_required
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
        categories = ArticleCategory.get_valid_categories()
        for c in categories:
            categories_data.append(
                dict(name=c.name,
                     id=c.id,
                     articles=[dict(title=a.title,
                                    id=a.id)
                               for a in Article.get_by_categoryid(c.id)]))
        return dict(
            data=categories_data,
            code=200,
            message="ok"
        )

    def post(self):
        (name, ) = get_params([
            Argument('name', type=str, required=True)
        ])
        new_category = ArticleCategory.insert(name)
        db.session.commit()
        return dict(
            id=new_category.id,
            code=200,
            message='ok'
        )
    
    def put(self):
        (category_id, new_name) = get_params([
            Argument('id', type=int, required=True),
            Argument('new_name', type=str, required=True)
        ])
        ArticleCategory.rename(category_id, new_name)
        db.session.commit()
        return dict()


    def delete(self):
        (category_id, ) = get_params([
            Argument('id', type=int, required=True)
        ])
        ArticleCategory.delete(category_id)
        db.session.commit()
        return dict()
