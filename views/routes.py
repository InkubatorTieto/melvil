from flask import render_template, flash, redirect
from . import library
from forms import LoginForm, SearchForm, ContactForm


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login')
def login():
    return render_template('login.html', title='Sign In', form=LoginForm())


@library.route('/search')
def search():
    return render_template('search.html', title='Search', form=SearchForm())


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Message send!')
        return redirect('/')
    return render_template('contact.html', title='Contact', form=form)
