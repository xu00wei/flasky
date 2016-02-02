#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import  render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from . import auth
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # 生成登入表单
    if form.validate_on_submit(): # 如果提交表单
        user = User.query.filter_by(email=form.email.data).first() # 查询数据库中的帐号
        if user is not None and user.verify_password(form.password.data): # 验证密码
            login_user(user, form.remember_me.data) # 存储是否自动登入信息
            return redirect(request.args.get('next') or url_for('main.index')) # 跳转原请求网页或首页
        flash('无效的用户名或密码') # 用户名不存在或密码错误
    return render_template('auth/login.html', form=form) # 重新输入登入信息

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的帐号', 'auth/email/confirm', user=user, token=token)
        flash('认证邮件已经发送至您的邮箱,请您在一个小时内完成认证!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登入。')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您已经认证了帐号，谢谢！')
    else:
        flash('该认证链接无效或者已经过期。')
    return redirect(url_for('main.index'))

# Flask-login 会拦截未登入用户的请求，把用户发往登入页面
@auth.route('/secret')
@login_required
def secret():
    return '抱歉，只有已登入的用户方能访问该网页！'

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的帐号', 'auth/email/confirm', user=current_user, token=token)
    flash('一个新的认证邮件已经发送到您的邮箱。')
    return redirect(url_for('main.index'))
