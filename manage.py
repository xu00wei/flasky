#-*- encoding:utf-8 -*-
#!/usr/bin/env python
# import os
import sys
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

reload(sys)
sys.setdefaultencoding('utf8')

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
manager = Manager(app)
Migrate = Migrate(app, db)

# 为python shell 定义上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
