from flask import Flask
from views import library
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
app = Flask(__name__)
app.config.from_object(DevConfig)
app.register_blueprint(library)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'jdbc:postgresql://localhost:5432/postgres'
db = SQLAlchemy(app)
'''alembic = Alembic()
alembic.init_app(app)
alembic.revision('making changes')
alembic.upgrade()
environment_context = alembic.env'''
