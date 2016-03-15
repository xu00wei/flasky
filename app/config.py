#-*- encoding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 获取该文本的绝对地址

# CSRF_ENABLED=True

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MyFristFlakyBlogKuangJiaLLL' # 可以在环境中设定，但提供一个默认值
    RESET_KEY = os.environ.get('RESET_KEY') or 'MyResetPasswordKeyWithFlaskHHH'
    FLASK_ADMIN = 'xu0.0wei@qq.com'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = 'True'
    FLASKY_MAIL_SUBJECT_PREFIX = 'Flasky'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_COMMENTS_PER_PAGE = 8
    FLASKY_COMMENTS_MANAGE_PER_PAGE = 25
    FLASKY_MAIL_SENDER = 'xu0.0wei@qq.com'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True # 启用传输层安全协议
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'xu0.0wei'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
