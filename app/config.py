#-*- encoding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 获取该文本的绝对地址

# CSRF_ENABLED=True

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # 可以在环境中设定，但提供一个默认值
    SQLALCHEMY_COMMIT_ON_TEARDOWN = 'True'

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
