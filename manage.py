#!/usr/bin/env python
# coding=utf-8
# from app import create_app,db
# from app.models import User #这里把需要初始化的表，对应的类拿出来
# from flask_script import Manager,Shell
# from flask_migrate import MigrateCommand,Migrate

# if __name__ == '__main__':
#     app = create_app('development')
#     manager = Manager(app)
#     migrate = Migrate(app,db)   #建立一个迁移数据库的对象。
#     def make_shell_context():
#         return dict(app=app,db=db,User=User)
#     manager.add_command('shell',Shell(make_context=make_shell_context)) #make_context的意义在于命令行中输入db就知道是我们创建的那个db
#     manager.add_command('db',MigrateCommand)

#     manager.run()
