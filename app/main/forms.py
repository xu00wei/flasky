#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, ValidationError
from ..models import User,Role

# class NameForm(Form):
    # name = StringField('您的名字是？', validators=[Required()])
    # submit = SubmitField('提交')

class EditProfileForm(Form):
    real_name = StringField('真实姓名', validators=[Length(0,64)])
    location = StringField('居住地址', validators=[Length(0,64)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')

class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    confirmed = BooleanField('已认证')
    role = SelectField('角色', coerce=int)
    real_name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('居住地址', validators=[Length(0,64)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱以经被注册过')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('该邮箱以经被注册过')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all() ]
        self.user = user

class PostForm(Form):
    body = TextAreaField('你想写什么', validators=[Required()])
    submit = SubmitField('Submit')

