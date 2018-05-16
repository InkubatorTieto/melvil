from flask import render_template
from . import library


@library.route('/')
def index():
    return render_template('index.html')
