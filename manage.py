from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from flask_script import Manager,Server
from app.models import User,Pitch,Comment
from  flask_migrate import Migrate, MigrateCommand
# Creating app instance

#app = create_app('development')
app = create_app('production')
db = SQLAlchemy(app)


manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
# db = SQLAlchemy()

manager.add_command('server',Server)
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User,Pitch = Pitch,Comment = Comment )

if __name__ == '__main__':
    manager.run()



# import flask_script
# import app
# from app import create_app,db
# from app.models import User, Role
# from flask_script import Manager
# from flask_sqlalchemy import SQLAlchemy

# app = create_app('development')
# manager = Manager(app)
# db = SQLAlchemy()



# @manager.shell
# def make_shell_context():
#     return dict(app = app,db = db,User = User,Role=Role )
# if __name__ == '__main__':
#     manager.run()    