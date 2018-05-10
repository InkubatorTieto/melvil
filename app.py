from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
app.register_blueprint(library)
db = SQLAlchemy(app)