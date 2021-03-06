#-*- encoding:utf-8 -*-
from flask.ext.httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from .errors import forbidden,unauthorized
from flask import g, jsonify
from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.confirm_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(email = email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@api.route('/token')
def get_token():
    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('无效的密令')
    return jsonify({'token':g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})

@auth.error_handler
def auth_error():
    return unauthorized('身份验证出错！')

@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('用户未认证邮箱')






@api.route('/comments/')
def get_comments():
    comments = Comment.query.filter().all()
    return jsonify([comment.to_json() for comment in comments])

@api.route('/comments/<int:id>')
def get_comment(id):
    user = User.query.filter_by(id=id).first()
    user.comments.order_by
