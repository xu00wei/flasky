#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, abort
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Permission
from flask.ext.login import login_required
from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form = form, name = session.get('name'),
                           known = session.get('known', False), current_time = datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

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

