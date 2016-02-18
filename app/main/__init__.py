# -*- encoding=utf-8 -*-
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors # 避免循环导入依赖

from ..models import Permission
@main.app_context_processor    # 将permission类添加到上下文中方便全局调用
def inject_permissions():
    return dict(Permission=Permission)
