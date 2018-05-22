from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)
    app.secret_key = os.urandom(24)
    db.init_app(app)
    return app
