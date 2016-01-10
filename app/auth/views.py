#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import  render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, login_user, logout_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from . import auth
from .. import db

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
        flash('你现在可以登入了')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登入。')
    return redirect(url_for('main.index'))

# Flask-login 会拦截未登入用户的请求，把用户发往登入页面
@auth.route('/secret')
@login_required
def secret():
    return '抱歉，只有已登入的用户方能访问该网页！'
