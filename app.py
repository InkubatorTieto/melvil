from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from raven import Client

db = SQLAlchemy()
sentry = Sentry()
client = Client()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)

    db.init_app(app)
    sentry.init_app(app)


    return app
