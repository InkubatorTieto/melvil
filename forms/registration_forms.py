from wtforms import StringField, PasswordField, SubmitField

from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name')
    surname = StringField('Surname')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')
