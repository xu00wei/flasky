#-*- encoding=utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from datetime import datetime
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager

# 加载用户的回调函数，若用户不存在则返回None
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0X04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0X80

class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), unique=True)
        default = db.Column(db.Boolean, index=True, default=False)
        permissions = db.Column(db.Integer)
        users = db.relationship('User', backref='role')

        @staticmethod
        def insert_roles():
            roles = {
                'User': (Permission.FOLLOW |
                         Permission.COMMENT |
                         Permission.WRITE_ARTICLES, True),
                'Moderator': (Permission.FOLLOW |
                              Permission.COMMENT |
                              Permission.WRITE_ARTICLES |
                              Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
            }
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()

        def __repr__(self):
            return '<Role %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    realname = db.Column(db.String(64))
    location = db.Column(db.String(128))
    about_me = db.Column(db.Text())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role_id = Role.query.filter_by(permissions=0xff).first().id
            else:
                self.role_id = Role.query.filter_by(default=True).first().id

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self): # 密码不可读取
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password): # 将password转换为hash密码
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password): # 比较密码是否相
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600): # 有效时限3600秒
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}) # 将自身id生成令牌字符串

    def generate_reset_password_token(self, expiration=3600):
        s = Serializer(current_app.config['RESET_KEY'], expiration)
        return s.dumps({'reset':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token) # 将令牌字符串反解析成数据(此处数据为id)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def confirm_reset(self, token):
        s = Serializer(current_app.config['RESET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        return True

    def up_date_time(self):
        self.last_login_date = datetime.utcnow()
        db.session.add(self)
