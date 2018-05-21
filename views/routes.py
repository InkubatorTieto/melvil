# from flask import render_template, redirect, flash
# from . import library
# from forms.forms import LoginForm, SearchForm, ContactForm, RegistrationForm
# from send_email.emails import send_email
# from config import DevConfig
# import os
#
#
# @library.route('/')
# def index():
#     return render_template('index.html', title='Welcome!')
#
#
# @library.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if not form.validate_on_submit():
#         pass
#     return render_template('login.html', title='Sign In', form=form, error=form.errors)
#
#
#
#
#
# @library.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash('Registration succeeded', 'ok')
#         return redirect('/register')
#     return render_template('registration.html', title='Register', form=form, error=form.errors)
