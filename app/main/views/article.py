from flask import jsonify
from flask_restful import reqparse

from app.models import Article
from . import main


@main.route('/articles/<int:id>', methods=['GET', 'POST'])
def articles(id):
    article = Article.query.get(id)
    if not article:
        
