from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email')#, validators=[DataRequired(), Email()])
    password = PasswordField('Password') #, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SearchForm(FlaskForm):
    query = StringField('Search')
    submit = SubmitField('Search')


class ContactForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    title = StringField('title', validators=[DataRequired()])
    message = TextAreaField('message', validators=[DataRequired()])
    send_message = SubmitField('Send message')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('confirmPass', message='Passwords must match.')])
    confirmPass = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
