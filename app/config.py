#-*- encoding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 获取该文本的绝对地址

# CSRF_ENABLED=True

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MyFristFlakyBlogKuangJiaLLL' # 可以在环境中设定，但提供一个默认值
    RESET_KEY = os.environ.get('RESET_KEY') or 'MyResetPasswordKeyWithFlaskHHH'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = 'True'
    FLASKY_MAIL_SUBJECT_PREFIX = 'Flasky'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SENDER = '1129116069@qq.com'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True # 启用传输层安全协议
    MAIL_USERNAME = '1129116069'
    MAIL_PASSWORD = 'pwemtncswvfabaaj'# 腾讯以授权码为密码

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:030034@localhost/flasky'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:030034@localhost/flasky'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://root:030034@localhost/flasky'

config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
