from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask_login import login_required, current_user

from app import db
from app.api.utils import get_params
from app.models import Article, ArticleCategory, PublishedArticle
from app.utils.data import date2stamp


class ArticlesResource(Resource):
    @login_required
    def post(self):
        (title, category_id) = get_params([
            Argument('title', type=str, required=True),
            Argument('category_id', type=int, required=True)
        ])
        new_article = Article.insert(
            title,
            category_id,
            current_user.id
        )
        db.session.commit()
        data = dict(
            code=200,
            message="ok",
            id=new_article.id
        )
        return data


class ArticlesIdResource(Resource):
    @login_required
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
                is_published=article.is_published,
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
            (title, content) = get_params([
                Argument('title', type=str, required=True),
                Argument('content', type=str, required=True)
            ])
            article.update(title, content)
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
            article.delete()
            db.session.commit()
            data = dict(
                code=200,
                message="ok"
            )
        return data


class ArticlePublishResource(Resource):
    @login_required
    def post(self, id):
        article = Article.query.get(id)
        if not article:
            data = dict(
                code=404,
                message="The requested article is not found"
            )
        else:
            (title, content, html, abscontent) = get_params([
                Argument('title', type=str, required=True),
                Argument('content', type=str, required=True),
                Argument('html', type=str, required=True),
                Argument('abscontent', type=str, required=True),
            ])
            article.update(title, content)
            article.publish(html, abscontent)
            data = dict(
                code=200,
                message="ok"
            )
            db.session.commit()
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
            article.unpublish()
            data = dict(
                code=200,
                message="ok"
            )
            db.session.commit()
        return data


class ArticleCategoriesResource(Resource):
    @login_required
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

    @login_required
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
    
    @login_required
    def put(self):
        (category_id, new_name) = get_params([
            Argument('id', type=int, required=True),
            Argument('new_name', type=str, required=True)
        ])
        ArticleCategory.rename(category_id, new_name)
        db.session.commit()
        return dict()

    @login_required
    def delete(self):
        (category_id, ) = get_params([
            Argument('id', type=int, required=True)
        ])
        ArticleCategory.delete(category_id)
        db.session.commit()
        return dict()
