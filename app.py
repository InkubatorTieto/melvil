from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:////tmp/test.db'

db = SQLAlchemy(app)

app.register_blueprint(library)
