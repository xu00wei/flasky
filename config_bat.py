#-*- encoding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 获取该文本的绝对地址

# class Config:
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # 可以在环境中设定，但提供一个默认值

    # SQLALCHMEY_COMMIT_ON_TEARDOWN = True # True 每次请求结束后都会自动提交数据库中的变动

    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]' # 定义邮件主题的前缀
    # FLASKY_MAIL_SENDER = 'Flasky Admin <FLASKY@example.com>' # 定义邮件发件人的地址

    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # @staticmethod
    # def init_app(app):
        # pass

# class DevelopmentConfig(Config):
    # DEBUG = True
    # MAIL_SERVER = 'smtp.googlmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        # 'mysql://' + os.path.join('root:030034@localhost/blog')

