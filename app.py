from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask import Flask
from views import library
from config import DevConfig
from flask_mail import Mail
from models import *
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.register_blueprint(library)
    db.init_app(app)
    '''with app.test_request_context():
        db.create_all()'''
    #db.drop_all()
    mail.init_app(app)
    return app
