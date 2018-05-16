from flask import render_template
from . import library
from send_email.emails import *


@library.route('/')
def index():
    send_email('Tieto-Library',
               'tieto.library@gmail.com',
               ['tieto.library@gmail.com'],
               '',
               render_template("registration_email.html"))

    return render_template('index.html')
