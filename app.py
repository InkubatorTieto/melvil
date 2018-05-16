from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask import Flask
from config import DevConfig
from flask_login import LoginManager
from views import library
import os

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)
    app.secret_key = os.urandom(24)
    db.init_app(app)
    login_manager.init_app(app)

    return app
