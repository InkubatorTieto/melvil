from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from forms.custom_validators import tieto_email, name, surname


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()],
                        render_kw=({'class': 'inputs', 'placeholder': 'Email'}))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=({'class': 'inputs', 'placeholder': 'Password'}))
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In',
                         render_kw=({'class': 'btn btn-primary submits'}))


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[Email()],
                        render_kw=({'class': 'inputs', 'placeholder': 'Email'}))
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(3), name],
                             render_kw=({'class': 'inputs', 'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[DataRequired(), Length(3), surname],
                          render_kw=({'class': 'inputs', 'placeholder': 'Surname'}))
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm_pass', message='Passwords must match.')],
                             render_kw=({'class': 'inputs', 'placeholder': 'Password'}))
    confirm_pass = PasswordField('Confirm password',
                                 validators=[DataRequired()],
                                 render_kw=({'class': 'inputs', 'placeholder': 'Confirm Password'}))
    submit = SubmitField('Submit',
                         render_kw=({'class': 'btn btn-primary submits'}))


class ContactForm(FlaskForm):
    email = StringField('email',
                        validators=[Email()],
                        render_kw=({'class': 'inputs', 'placeholder': 'Email'}))
    title = StringField('title',
                        validators=[DataRequired()],
                        render_kw=({'class': 'inputs', 'placeholder': 'Title'}))
    message = TextAreaField('message',
                            validators=[DataRequired()],
                            render_kw=({'class': 'inputs message', 'placeholder': 'Message'}))
    send_message = SubmitField('Send message',
                               render_kw=({'class': 'btn btn-primary submits'}))


class SearchForm(FlaskForm):
    query = StringField('Search')
    submit = SubmitField('Search')


class ForgotPass(FlaskForm):
    email = StringField('email', validators=[Email()], render_kw=({'class': 'inputs', 'placeholder': 'Email'}))
    submit = SubmitField('Submit',
                         render_kw=({'class': 'btn btn-primary submits'}))


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit',
                         render_kw=({'class': 'btn btn-primary submits'}))
