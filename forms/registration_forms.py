from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name')
    surname = StringField('Surename')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')
