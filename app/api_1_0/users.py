from . import api
from ..models import User, Post
from flask import request, jsonify, url_for, current_app

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
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


@api.route('/users/<int:id>/followed-posts/')
def get_user_followed_posts(id):
    user = User.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['FLASKY_POSTS_PER_PAGE'])
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_user_followed_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_user_followed_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev_page': prev_page,
        'next_page': next_page,
        'count': pagination.total
    })
