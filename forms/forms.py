from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SearchForm(FlaskForm):
    query = StringField('Search')
    submit = SubmitField('Search')


class ContactForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    message = TextAreaField('message', validators=[DataRequired()])
    send_message = SubmitField('Send message')


class RegistrationForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name')
    surname = StringField('Surname')
    password = PasswordField('Password')
    confirmPass = PasswordField('Confirm password')
    submit = SubmitField('Sign In')