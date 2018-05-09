from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevConfig)
app.register_blueprint(library)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import models
