from flask import Flask
from config import DevConfig, ProdConfig
from views import library
from views.book import library_books
import os
from views.index import login_manager
from init_db import db
from raven.contrib.flask import Sentry
from raven import Client
from flask_mail import Mail
import time

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
    login_manager.init_app(app)
    mail.init_app(app)

    db_not_ready = True
    while (db_not_ready):
        try:
            db.init_app(app)
            with app.app_context():
                db.create_all()
            db_not_ready = False
        except:
            print("DB not ready!")
            print("Polling DB..")
            time.sleep(1)
    return app
