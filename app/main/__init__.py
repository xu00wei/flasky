# -*- encoding=utf-8 -*-
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors # 避免循环导入依赖

