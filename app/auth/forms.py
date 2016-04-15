#-*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User
NOT_NONE="该输入框不能为空!"
INVALID_EMAIL_ADDRESS="无效的邮件地址!"
class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(message=NOT_NONE), Length(1, 64), Email(message=INVALID_EMAIL_ADDRESS)])
    password = PasswordField('密码', validators=[Required(message=NOT_NONE)])
    remember_me = BooleanField('下次自动登入')
    submit = SubmitField('登入')

class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(message=NOT_NONE), Length(1, 64), Email(message=INVALID_EMAIL_ADDRESS)])
    username = StringField('用户名', validators=[Required(message=NOT_NONE), Length(1,64)])
    password = PasswordField('密码', validators=[Required(message=NOT_NONE), EqualTo('password2', message='两次密码必须一致！')])
    password2 = PasswordField('确认密码', validators=[Required(message=NOT_NONE)])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册过了哦～')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用了')

class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required(message=NOT_NONE)])
    password = PasswordField('新密码', validators=[Required(message=NOT_NONE), EqualTo('password2', message='新密码的两次输入必须一致！')])
    password2 = PasswordField('确认密码', validators=[Required(message=NOT_NONE)])
    submit = SubmitField('修改')

class ResetPasswordRequiredForm(Form):
    email = StringField('邮箱', validators=[Required(message=NOT_NONE), Email(message=INVALID_EMAIL_ADDRESS)])
    submit = SubmitField('注册')

class ResetPasswordForm(Form):
    email = StringField('邮箱', validators=[Required(message=NOT_NONE), Email(message=INVALID_EMAIL_ADDRESS)])
    password = PasswordField('新密码', validators=[Required(message=NOT_NONE),EqualTo('password2', message='新密码的两次输入必须一致！')])
    password2 = PasswordField('确认密码', validators=[Required(message=NOT_NONE)])
    submit = SubmitField('重置')
