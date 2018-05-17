from flask import render_template, request, session
from . import library
from models.user import User
from forms.login_form import LoginForm
from forms.registration_forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import current_user, LoginManager

login_manager = LoginManager()


@library.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return user_id


@library.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated: # Coś nie bangla :/
            return "You are already logged"
        else:
            form = LoginForm()
            return render_template('login.html', form=form)
    else:
        form = LoginForm()
        # try:
        if form.validate():
            data = User.query.filter_by(email=form.email.data).first()
            if data is not None and check_password_hash(data.password_hash, form.password.data):
                print(data.email)
                load_user(data.email)
                return render_template('index.html')
            else:
                return 'Login failed'
        else:
            return 'Incorrect data'
        # except:
        #     return 'Something went wrong'




@library.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        form = RegistrationForm()
        print(form)
        return render_template('registration.html', form=form)
    else:
        form = RegistrationForm()
        if form.validate():
            try:
                new_user = User(email=form.email.data, first_name=form.first_name.data, surname=form.surname.data,
                                password_hash=generate_password_hash(form.password.data))
                print("TO JA:", new_user)
                db.session.add(new_user)
                db.session.commit()
            except:
                return 'Registration failed'
        return 'The registration was successful'