#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request, make_response, session
# from datetime import datetime
from . import main
from .forms import PostForm, EditProfileForm, EditProfileAdminForm, EditPostForm, CommentForm
from .. import db
from ..models import User, Permission, Role, Post, Comment
from flask.ext.login import login_required, current_user, current_app
from ..decorators import admin_required, permission_required

# @main.route('/', methods=['GET','POST'])
# def index():
    # form = NameForm()
    # if form.validate_on_submit():
        # user = User.query.filter_by(username=form.name.data).first()
        # if user is None:
            # user = User(username = form.name.data)
            # db.session.add(user)
            # session['known'] = False
        # else:
            # session['known'] = True
        # session['name'] = form.name.data
        # form.name.data = ''
        # return redirect(url_for('.index'))
    # return render_template('index.html', form = form, name = session.get('name'),
                           # known = session.get('known', False), current_time = datetime.utcnow())

@main.route('/', methods=['GET', 'POST'])
def index():
    # form = PostForm()
    # if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        # post = Post(body=form.body.data,
                    # author=current_user._get_current_object())
        # db.session.add(post)
        # return redirect(url_for('.index'))
    # show_followed = False
    # if current_user.is_authenticated:
        # show_followed = bool(request.cookies.get('show_followed', ''))
    # if show_followed:
        # query = current_user.followed_posts
    # else:
    #     query = Post.query
    query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'])
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    posts = pagination.items
    return render_template('index1.html', posts=posts, pagination=pagination, show_followed=show_followed)

@main.route('/look-around')
def look_around():
    resp = make_response(redirect(url_for('.test')))
    resp.set_cookie('INDEX_POST_VIEW','look-around', max_age=3600)
    return resp

@main.route('/hot')
def read_hot():
    resp = make_response(redirect(url_for('.test')))
    resp.set_cookie("INDEX_POST_VIEW",'read-hot',max_age=3600)
    return resp

@main.route('/new-posts')
def new_posts():
    resp = make_response(redirect(url_for('.test')))
    resp.set_cookie('INDEX_POST_VIEW','new', max_age=3600)
    return resp

@main.route('/test', methods=['GET', 'POST'])
def test():
    # print "this is test"
    page = request.args.get('page', 1, type=int)
    query = Post.query
    # print request.cookies.get('INDEX_POST_VIEW')
    # print "------------------------"
    post_view = request.cookies.get('INDEX_POST_VIEW')
    if post_view is None:
        post_view = 'new'

    if post_view == 'look-around':
        pagination = query.order_by(Post.timestamp).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'])
    elif post_view == 'read-hot':
        pagination = query.order_by(Post.read.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'])
    else:
        pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'])
    posts = pagination.items
    # print post_view
    return render_template('index2.html', posts=posts, pagination=pagination, post_view=post_view)

@main.route('/writing', methods=['GET', 'POST'])
def writing():
    form = PostForm(request.form)
    # print form.validate_on_submit()
    # print form.errors
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user._get_current_object(),
                    read = 0)
        db.session.add(post)
        return redirect(url_for(".user_posts", username = current_user.username))
    return render_template('writing.html', form=form)

@main.route('/ppt')
def ppt():
    return render_template('ppt.html')

@main.route('/post/<int:id>', methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    page = request.args.get('page',1, type=int)
    per_page = current_app.config['FLASKY_COMMENTS_PER_PAGE']
    post.read += 1
    db.session.add(post)
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash('你需要登入才能评论')
            return redirect(url_for('auth.login'))
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object(),
                          )
        db.session.add(comment)
        flash('评论提交成功')
        return redirect(url_for('.post', id = post.id, page=page))
    censor = current_user.can(Permission.MODERATE_COMMENTS)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
         page, per_page=per_page, error_out=False
    )
    comments = pagination.items
    return render_template('post.html', post=post, user=post.author, form=form, comments=comments, pagination=pagination, censor=censor)

@main.route('/edit-post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = EditPostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        db.session.add(post)
        flash('编辑成功＾－＾')
        return redirect(url_for('.post', id=id))
    form.body.data = post.body
    form.title.data = post.title
    return render_template('writing.html', form=form)

@main.route('/comment-manage')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def comment_manage():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['FLASKY_COMMENTS_MANAGE_PER_PAGE']
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page,per_page,error_out=False)
    comments = pagination.items
    return render_template('comment_manage.html', comments = comments, pagination = pagination, page = page)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template("user_posts.html", user=user, posts=posts)
   #  print len(posts)
    # if session.get('posts_request') is True:
        # session['posts_request'] = False
        # return render_template('user_posts.html', user=user, posts=posts)
    # return render_template('user.html',user=user, posts=posts)

@main.route('/test/<username>')
def test_username(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)

@main.route('/user/<username>/posts')
def user_posts(username):
    session['posts_request'] = True
    return redirect(url_for('.user', username=username))

@main.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.real_name = form.real_name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('您的个人资料已经更新')
        return redirect(url_for('.user', username=current_user.username))
    form.real_name.data = current_user.real_name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.real_name = form.real_name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('用户资料已经更新成功')
        return redirect(url_for('.user', username = user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.real_name.data = user.real_name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "当你看到这段文字，你已经拥有了管理员的权限！"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "当你看到这段文字，你已经拥有了审核人的权限！"


@main.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    return redirect(request.referrer)

@main.route('/unfollow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    return redirect(request.referrer)

@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=20)
    follows = [{'user':item.follower, 'timestamp':item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, endpoint='.followers', pagination=pagination, follows=follows)

@main.route('/followeds/<username>')
def followeds(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page)
    followeds = [{'user':item.followed, 'timestamp':item.timestamp}
                 for item in pagination.items]
    return render_template('followers.html', user=user, endpoint='.followeds', follows = followeds, pagination=pagination)

@login_required
@main.route('/followed')
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1', max_age=60*60)
    return resp

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','', max_age=60*60)
    return resp

@main.route('/comment-manager/able_or_not/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def able_or_not(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = not comment.disabled
    db.session.add(comment)
    return redirect(request.referrer)
