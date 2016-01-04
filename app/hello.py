#-*- coding:utf-8 -*-
import os
import sys
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from main.forms import NameForm

reload(sys)
sys.setdefaultencoding('utf-8')

basedir  = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
app.config.from_object('config')

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
       old_name = session.get('name')
       if old_name is not None and old_name != form.name.data:
           flash('Looks like you have changed your name!')
       session['name'] = form.name.data
       return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

db = SQLAlchemy(app)

# 启动管理
if __name__ == '__main__':
    manager.run()

