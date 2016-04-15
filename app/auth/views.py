#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import  current_app, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordRequiredForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ..models import User
from . import auth
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # 生成登入表单
    if form.validate_on_submit(): # 如果提交表单
        user = User.query.filter_by(email=form.email.data).first() # 查询数据库中的帐号
        print user
        if user is not None and user.verify_password(form.password.data): # 验证密码
            if not user.confirmed:
                uid = user.generate_auth_id_token()
                return redirect(url_for('auth.unconfirmed', uid=uid))
            login_user(user, form.remember_me.data) # 存储是否自动登入信息
            return redirect(url_for('main.test')) # 跳转原请求网页或首页
        flash('无效的用户名或密码') # 用户名不存在或密码错误
    return render_template('auth/login.html', form=form) # 重新输入登入信息


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
   #  print form.validate_on_submit()
    # print not form.validate_email(form.email)
    # print not form.validate_username(form.username)

    if form.validate_on_submit() \
    and not form.validate_email(form.email) \
    and not form.validate_username(form.username):
        print "??"
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的帐号', 'auth/email/confirm', user=user, token=token)
        flash('认证邮件已经发送至您的邮箱,请您在一个小时内完成认证!')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
def confirm(token):

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token) # 将令牌字符串反解析成数据(此处数据为id)
    except:
        flash('该认证链接无效或者已经过期。')
        return redirect(url_for('main.index'))

    uid = data.get('confirm')
    user = User.query.filter_by(id=uid).first()

    if user.confirmed:
        return redirect(url_for('main.index'))

    if user:
        user.confirmed = 1
        db.session.add(user)
        flash('邮箱验证成功, 请输入帐号密码登入')
        return redirect(url_for("auth.login"))
    else:

        flash('该认证链接无效或者已经过期。')
        return redirect(url_for('main.index'))
# confirmed \
        # and request.endpoint[:5] != 'auth.' \
        # and request.endpoint != 'static':
            # return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed/<uid>')
def unconfirmed(uid):
    if not current_user.is_anonymous and current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html', uid = uid)

@auth.route('/remail/<uid>')
def resend_confirmation(uid):
    user = User.confirm_uid_token(uid)
    token = user.generate_confirmation_token()
    send_email(user.email, '确认您的帐号', 'auth/email/confirm', user=user, token=token)
    flash('一个新的认证邮件已经发送到您的邮箱。')
    return redirect(url_for('auth.unconfirmed', uid=uid))

@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('密码修改成功！')
            return redirect(url_for('main.index'))
        else:
            flash('旧密码错误')
    return render_template('auth/change_password.html', form = form)

@auth.route('/reset-password', methods=['GET','POST'])
def reset_password_required():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequiredForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            send_email(user.email, '重设密码', 'auth/email/reset_password', user=user, token=token )
            flash('设置密码的的邮件已经发送到您邮件，请注意查收。')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_required.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.confirm_reset(token):
            user.password = form.password.data
            db.session.add(user)
            flash('密码已经重新设置，快去登入吧！')
            return redirect(url_for('auth.login'))
        else:
            flash('您的邮箱有误！')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

