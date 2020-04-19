from app import app, db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app.models import User, Todo

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell)
manager.add_command('runserver', Server(
    use_debugger = False,
    use_reloader = True,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()