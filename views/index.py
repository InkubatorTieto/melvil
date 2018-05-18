from flask import render_template, request
from . import library
from models.user import User
from itsdangerous import URLSafeTimedSerializer
from forms.registration_forms import RegistrationForm
from werkzeug.security import generate_password_hash
from app import db
from send_email import send_confirmation_email
from config import DevConfig


@library.route('/')
def index():
    return render_template('index.html')


@library.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('registration.html', form=form)
    else:
        form = RegistrationForm()
        if form.validate():
            try:
                new_user = User(email=form.email.data,
                                first_name=form.first_name.data,
                                surname=form.surname.data,
                                password_hash=generate_password_hash(form.password.data))
                print("TO JA:", new_user)
                db.session.add(new_user)
                db.session.commit()
                print(new_user.email)
                send_confirmation_email(new_user.email)
            except:
                return 'Registration failed'
        return 'The registration was successful'


@library.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)
        email = confirm_serializer.loads(token,
                                         salt=DevConfig.SECURITY_PASSWORD_SALT,
                                         max_age=3600)
    except:
        return 'The confirmation link is invalid or has expired.', 'error'

    user = User.query.filter_by(email=email).first()

    if user.active:
        return 'Account already confirmed. Please login.'
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        return 'Thank you for confirming your email address!'
