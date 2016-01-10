#-*- coding:utf-8 -*-
import os
import sys
from flask import Flask, render_template, session, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from main.forms import NameForm

reload(sys)
sys.setdefaultencoding('utf-8')

basedir  = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
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
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 启动管理
if __name__ == '__main__':
    manager.run()

