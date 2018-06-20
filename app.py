import os
import time

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from raven import Client
from raven.contrib.flask import Sentry

from config import DevConfig, ProdConfig
from init_db import db, ma
from views.book import library_books
from views.index import library
from views.book import library_books
from utils.xlsx_reader import get_books, get_magazines
from xlsx_reader import get_books, get_magazines

mail = Mail()
sentry = Sentry()
client = Client()

if os.getenv('APP_SETTINGS', '') == 'prod':
    config_env = ProdConfig
else:
    config_env = DevConfig


def create_app(config=config_env):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(library)
    app.register_blueprint(library_books)
    app.secret_key = os.urandom(24)
    mail.init_app(app)

    db_not_ready = True
    while db_not_ready:
        try:
            db.init_app(app)
            with app.app_context():
                db.create_all()
            db_not_ready = False
        except:
            print("DB not ready!")
            print("Polling DB..")
            time.sleep(1)
    ma.init_app(app)
    return app


app = create_app()
migrate = Migrate(app, db)


@app.cli.command(with_appcontext=True)
def load_xls_into_db():
    get_magazines('./biblioteka_probna.xlsx')
    get_books('./biblioteka_probna.xlsx')


app.cli.add_command(load_xls_into_db)

create_app(DevConfig)
