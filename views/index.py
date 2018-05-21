from flask import render_template, request, session
from flask_login import LoginManager
from forms.login_form import LoginForm
from forms.registration_forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import library
from models.user import User
from app import db
login_manager = LoginManager()


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm()
        try:
            if form.validate():
                data = User.query.filter_by(email=form.email.data).first()
                if data is not None and check_password_hash(data.password_hash, form.password.data):
                    session['logged_in'] = True
                    session['id'] = data.id
                    session['email'] = data.email
                    return render_template('index.html', session=session)
                else:
                    return 'Login failed'
            else:
                return 'Incorrect data'
        except request.exceptions.RequestException as e:
            return 'Something went wrong'


@library.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html', form=form)
    else:
        form = RegistrationForm()
        if form.validate():
            try:
                new_user = User(email=form.email.data, first_name=form.first_name.data, surname=form.surname.data,
                                password_hash=generate_password_hash(form.password.data))
                db.session.add(new_user)
                db.session.commit()
            except request.exceptions.RequestException as e:
                return 'Registration failed'
        return 'The registration was successful'
