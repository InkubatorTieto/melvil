from flask_mail import Mail
from flask import Flask
from config import DevConfig
from views import library
import os
from views.index import login_manager
from init_db import db

mail = Mail()


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(library)
    app.secret_key = os.urandom(24)

    db.init_app(app)
    with app.app_context():
        db.create_all()


    login_manager.init_app(app)
    mail.init_app(app)

    return app

import init_db