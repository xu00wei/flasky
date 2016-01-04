#-*- encoding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 获取该文本的绝对地址

CSRF_ENABLED=True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' # 可以在环境中设定，但提供一个默认值
