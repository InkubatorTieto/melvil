from config import DevConfig
from flask import render_template, request, session, redirect, flash
from flask_login import LoginManager
from forms.forms import LoginForm, SearchForm, ContactForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import render_template
from . import library
from models.users import User
from init_db import db
from send_email import send_confirmation_email
import os
from send_email.emails import *


login_manager = LoginManager()


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'logged_in' in session:
            return "You are already logged"
        else:
            form = LoginForm()
            return render_template('login.html', form=form, error=form.errors)
    else:
        form = LoginForm()
        try:

            if form.validate_on_submit():
                data = User.query.filter_by(email=form.email.data).first()
                if data is not None and check_password_hash(data.password_hash, form.password.data): # and data.active:
                    session['logged_in'] = True
                    session['id'] = data.id
                    session['email'] = data.email
                    return render_template('index.html', session=session)
                else:
                    return 'Login failed' # Łukasz napisze do tego komunikat
            else:
                return render_template('login.html', title='Sign In', form=form, error=form.errors)
        except:
            return 'Something went wrong'


@library.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html', form=form, error=form.errors)
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                new_user = User(email=form.email.data, first_name=form.first_name.data, surname=form.surname.data,
                                password_hash=generate_password_hash(form.password.data))
                db.session.add(new_user)
                db.session.commit()
                send_confirmation_email(new_user.email)
            except request.exceptions.RequestException as e:
                return 'Registration failed'
        else:
            return render_template('registration.html', title='Register', form=form, error=form.errors)
        return 'The registration was successful'


@library.route('/search')
def search():
    return render_template('search.html', title='Search', form=SearchForm())


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Message send', 'ok')
        try:
            email_template = open('./templates/emails/contact_confirmation.html', 'r').read()
        except:
            email_template = open(os.path.abspath(os.curdir) + './templates/emails/contact_confirmation.html',
                                  'r').read()
        send_email(
            'Contact confirmation, title: '+form.title.data,
            DevConfig.MAIL_USERNAME,
            [form.email.data],
            None,
            email_template)
        send_email(
            'Contact form: ' + form.title.data,
            DevConfig.MAIL_USERNAME,
            [DevConfig.MAIL_USERNAME],
            'Send by: '+form.email.data+'\n\n'+form.message.data,
            None)
        return redirect('/contact')
    return render_template('contact.html',
                           title='Contact',
                           form=form,
                           error=form.errors)


@library.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@library.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt='email-confirmation-salt',
                                         max_age=3600)
    except RuntimeError:
        return 'The confirmation link is invalid or has expired.', 'error'

    user = User.query.filter_by(email=email).first()

    if user.active:
        return 'Account already confirmed. Please login.'
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        return 'Thank you for confirming your email address!'



