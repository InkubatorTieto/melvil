from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_mail import Mail
from flask import Flask
from config import DevConfig
from views import library


mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)
    db.init_app(app)
    mail.init_app(app)

    return app
