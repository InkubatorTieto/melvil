from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegistrationForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name')
    surname = StringField('Surename')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')
