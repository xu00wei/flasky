# -*- encoding=utf-8 -*-
from functools import wraps
from flask import g
from .errors import forbidden

def permission_required(permissions):
    def decorators(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permissions):
                return forbidden('权限不足')
            return f(*args, **kwargs)
        return decorated_function
    return decorators
