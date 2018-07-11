from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from app import app, db, mail
from app.models import *


def make_shell_context():
    return dict(
        app=app,
        db=db,
        mail=mail,
        User=User,
        Article=Article
    )

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0', port=5005))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
