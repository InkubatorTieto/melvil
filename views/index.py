from flask import render_template
from . import library
from emails import *

@library.route('/')
def index():
    #send_email('Tieto-Library', 'tieto.library@gmail.com', ['tieto.library@gmail.com'], '', '<b>Dear sir/ms</b>body')

    return render_template('index.html')
