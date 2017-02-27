from . import api
from ..models import Comment, Post
from flask import jsonify, request, url_for, current_app

@api.route('/comments/')
def get_comments_json():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter().paginate(page, current_app.config['FLASKY_COMMENTS_MANAGE_PER_PAGE'], error_out=False)
    comments = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_comments', page = page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_comments', page = page + 1)
    return jsonify({
        'posts':[comment.to_json() for comment in comments],
        'prev_page': prev_page,
        'next_page': next_page,
        'count': pagination.total
    })

@api.route('/posts/<int:id>/comments/')
def get_post_comments(id):
    post = Post.query.filter_by(id=id).first()
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp).\
        paginate(page, current_app.config['FLASKY_COMMENTS_MANAGE_PER_PAGE'], error_out=False)
    comments = pagination.items
    prev_page, next_page = None, None
    if pagination.has_prev:
        prev_page = page - 1
    if pagination.has_next:
        next_page = page + 1
    return jsonify({
        'comments':[comment.to_json() for comment in comments],
        'prev_page': prev_page,
        'next_page': next_page,
        'count': pagination.total
})

@api.route('/comments/<int:id>')
def get_comment_json(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
