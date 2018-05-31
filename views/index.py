from config import DevConfig
from flask import render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager
from forms.forms import (
    LoginForm,
    SearchForm,
    ContactForm,
    RegistrationForm,
    ForgotPass,
    PasswordForm
)
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from . import library
from models.users import User
from init_db import db
from send_email import send_confirmation_email, send_password_reset_email
import os
from send_email.emails import send_email

login_manager = LoginManager()


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'logged_in' in session:
            message_body = 'You are already logged in.'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
        else:
            form = LoginForm()
            return render_template('login.html',
                                   form=form,
                                   error=form.errors)
    else:
        form = LoginForm()
        try:

            if form.validate_on_submit():
                data = User.query.filter_by(email=form.email.data).first()
                if (data is not None and
                        check_password_hash(data.password_hash,
                                            form.password.data) and
                        data.active):

                        session['logged_in'] = True
                        session['id'] = data.id
                        session['email'] = data.email
                        return render_template('index.html', session=session)
                else:
                    message_body = 'Login failed or ' \
                                   'your account is not activated'
                    message_title = 'Error!'
                    return render_template('message.html',
                                           message_title=message_title,
                                           message_body=message_body)
            else:
                return render_template('login.html',
                                       title='Sign In',
                                       form=form,
                                       error=form.errors)
        except:
            message_body = 'Something went wrong'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)


@library.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html',
                               form=form,
                               error=form.errors)
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            try:
                data = User.query.filter_by(email=form.email.data).first()
                if data is None:
                    new_user = User(
                        email=form.email.data,
                        first_name=form.first_name.data,
                        surname=form.surname.data,
                        password_hash=generate_password_hash(
                            form.password.data))
                    db.session.add(new_user)
                    db.session.commit()
                    send_confirmation_email(new_user.email)
                else:
                    message_body = 'User already exist'
                    message_title = 'Opss!'
                    return render_template('message.html',
                                           message_title=message_title,
                                           message_body=message_body)
            except:
                message_body = 'Registration failed'
                message_title = 'Error!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
        else:
            return render_template('registration.html',
                                   form=form,
                                   error=form.errors)
        message_body = 'The registration was successful.'
        message_title = 'Success!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)


@library.route('/search')
def search():
    return render_template('search.html', title='Search', form=SearchForm())


@library.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            email_template = open(
                './templates/contact_confirmation.html', 'r').read()
        except:
            email_template = open(os.path.abspath(os.curdir) +
                                  './templates/contact_confirmation.html',
                                  'r').read()
        send_email(
            'Contact confirmation, title: ' + form.title.data,
            DevConfig.MAIL_USERNAME,
            [form.email.data],
            None,
            email_template)
        send_email(
            'Contact form: ' + form.title.data,
            DevConfig.MAIL_USERNAME,
            [DevConfig.MAIL_USERNAME],
            'Send by: ' + form.email.data + '\n\n' + form.message.data,
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
        message_body = 'The confirmation link is invalid or has expired.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)

    user = User.query.filter_by(email=email).first()

    if user.active:
        message_body = 'Account already confirmed. Please login.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        message_body = 'Thank you for confirming your email address!'
        message_title = 'Success!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)


@library.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ForgotPass()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.active:
                send_password_reset_email(user.email)
                message_body = 'Please check your email \
                                for a password reset link.'
                message_title = 'Success!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
            else:
                message_body = 'Your email address must be confirmed \
                                before attempting a password reset.'
                message_title = 'Error!'
                return render_template('message.html',
                                       message_title=message_title,
                                       message_body=message_body)
        else:
            message_body = "This email doesn't exist"
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)
    return render_template('forgot_pass.html', form=form, error=form.errors)


@library.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(
            DevConfig.SECRET_KEY)
        email = password_reset_serializer.loads(token,
                                                salt='password-reset-salt',
                                                max_age=3600)
    except RuntimeError:
        message_body = 'The password reset link is invalid or has expired.'
        message_title = 'Error!'
        return render_template('message.html',
                               message_title=message_title,
                               message_body=message_body)

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except ValueError:
            message_body = 'Invalid email address!'
            message_title = 'Error!'
            return render_template('message.html',
                                   message_title=message_title,
                                   message_body=message_body)

        user.password_hash = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('library.login'))

    return render_template('reset_password_with_token.html',
                           form=form,
                           token=token,
                           error=form.errors)
