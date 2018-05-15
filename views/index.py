from flask import render_template
from . import library


@library.route('/')
def index():
    return render_template('index.html')

@library.route('/login')
def login():
    return render_template('login.html')

@library.route('/register')
def register():
    return render_template('register.html')

@library.route('/search')
def search():
    return render_template('browse.html')


@library.route('/logout')
def logout():
    pass


