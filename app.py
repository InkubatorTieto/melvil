from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)

    db.init_app(app)

    return app


mail = Mail(create_app())




