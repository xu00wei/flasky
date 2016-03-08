# -*- encoding=utf-8 -*-
from .decorators import permission_required
from . import api
from flask import request, url_for, current_app, jsonify, g
from ..models import Post, Permission
from .errors import forbidden
from .. import db

@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev_page': prev_page,
        'next_page': next_page,
        'count': pagination.total
    })

@api.route('/posts/<int:id>', methods=['GET','PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def get_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return forbidden('你没有编辑该文章的权限')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
