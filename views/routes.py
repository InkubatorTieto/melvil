from flask import render_template
from . import library
from forms import LoginForm, SearchForm


@library.route('/')
def index():
    return render_template('index.html')

@library.route('/login')
def login():
    return render_template('login.html', title='Sign In', form=LoginForm())

@library.route('/search')
def search():
    return render_template('search.html', title='Search', form=SearchForm())
