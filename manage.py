import unittest

from werkzeug.utils import cached_property

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database.models import db
from app.run import create_app


app = create_app()
app.app_context().push()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('./test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1



if __name__ == '__main__':
    manager.run()