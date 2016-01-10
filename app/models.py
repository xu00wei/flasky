#-*- encoding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask.ext.login import UserMixin
from . import login_manager

# 加载用户的回调函数，若用户不存在则返回None
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self): # 密码不可读取
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password): # 将password转换为hash密码
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password): # 比较密码是否相等
        return check_password_hash(self.password_hash, password)

