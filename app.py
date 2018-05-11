from flask import Flask
from views import library
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
app.register_blueprint(library)
