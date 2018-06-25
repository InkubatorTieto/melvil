import os
import time

from raven import Client
from raven.contrib.flask import Sentry

from flask import Flask
from flask_mail import Mail

from config import DevConfig, ProdConfig
from init_db import db, ma
from views.index import library
from views.book import library_books
from utils.xlsx_reader import get_books, get_magazines
from views.book_borrowing_dashboard import library_book_borrowing_dashboard


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
    app.register_blueprint(library_book_borrowing_dashboard)
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


@app.cli.command(with_appcontext=True)
def load_xls_into_db():
    get_magazines('./library_example.xlsx')
    get_books('./library_example.xlsx')


app.cli.add_command(load_xls_into_db)


create_app(DevConfig)
