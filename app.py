import os
import time

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from raven import Client
from raven.contrib.flask import Sentry
from sqlalchemy.exc import OperationalError, TimeoutError

from config import DevConfig, ProdConfig
from init_db import db
from ldap_utils.ldap_utils import register_hooks, ldap_client
from utils.xlsx_reader import get_books, get_magazines
from utils.create_admin_user import create_super_user
from views.book import library_books
from views.book_borrowing_dashboard import library_book_borrowing_dashboard
from views.index import library

mail = Mail()
sentry = Sentry()
client = Client()

if os.getenv('FLASK_ENV', '') == 'development':
    config_env = DevConfig
else:
    config_env = ProdConfig


def create_app(config=config_env):
    app = Flask(__name__)
    app.config.from_object(config)
    register_hooks(app)
    app.register_blueprint(library)
    app.register_blueprint(library_books)
    app.register_blueprint(library_book_borrowing_dashboard)
    app.secret_key = os.urandom(24)
    ldap_client.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    wait_for_db(app)
    return app


def wait_for_db(app):
    counter = 0
    with app.app_context():
        while counter < 30:
            try:
                r = db.engine.execute('SELECT 1')
                r.close()
                print('DB ready!')
                return
            except (ValueError, OperationalError):
                counter += 1
                print('DB not ready!\nRetry...')
                time.sleep(1)
            except KeyboardInterrupt:
                return
        raise TimeoutError('DB not ready!\nTimed out.')


app = create_app()
migrate = Migrate(app, db)


@app.cli.command('load_xls_into_db', with_appcontext=True)
def load_xls_into_db():
    get_magazines('./lib-data.xlsx')
    get_books('./lib-data.xlsx')


app.cli.add_command(load_xls_into_db)


@app.cli.command('create_admin', with_appcontext=True)
def create_admin():
    create_super_user()


app.cli.add_command(create_admin)
