from flask import render_template
from . import library
from send_email.emails import *


@library.route('/')
def index():
    return render_template('index.html')
