from datetime import datetime

from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm

from forms.custom_validators import (
    tieto_email,
    name,
    surname,
    check_password,
    check_pub_date
)


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), tieto_email],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Email'}))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'Password'}))
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In',
                         render_kw=({'class': 'btn btn-primary submits'}))


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[tieto_email],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Email'}))
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(3), name],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[DataRequired(), Length(3), surname],
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Last Name'}))
    password = PasswordField(
        'Password',
        validators=[DataRequired(), check_password,
                    EqualTo('confirm_pass',
                            message='Passwords must match.')],
        render_kw=({'class': 'inputs',
                    'placeholder': 'Password'}))
    confirm_pass = PasswordField(
        'Confirm password',
        validators=[DataRequired(), check_password],
        render_kw=({'class': 'inputs',
                    'placeholder': 'Confirm Password'}))
    submit = SubmitField('Sign Up',
                         render_kw=({'class': 'btn btn-primary submits'}))


class EditPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw=({'class': 'inputs',
                    'placeholder': 'Password'}))
    new_password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    EqualTo('confirm_pass',
                            message='Passwords must match.')],
        render_kw=({'class': 'inputs',
                    'placeholder': 'New Password'}))
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired()],
        render_kw=({'class': 'inputs',
                    'placeholder': 'Confirm Password'}))
    submit = SubmitField('Save',
                         render_kw=({'class': 'btn btn-primary submits'}))


class ContactForm(FlaskForm):
    email = StringField('email',
                        validators=[Email()],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Email'}))
    title = StringField('title',
                        validators=[DataRequired()],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Title'}))
    message = TextAreaField('message',
                            validators=[DataRequired()],
                            render_kw=({'class': 'inputs message',
                                        'placeholder': 'Message'}))
    send_message = SubmitField(
        'Send message',
        render_kw=({'class': 'btn btn-primary submits'}))


class SearchForm(FlaskForm):
    query = StringField('Search',
                        render_kw=({'class': 'form-control',
                                    'type': 'text',
                                    'placeholder': 'Search...'}))
    submit = SubmitField('Search')


class ForgotPass(FlaskForm):
    email = StringField('email',
                        validators=[tieto_email],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Enter Email Address'}))
    submit = SubmitField('Submit',
                         render_kw=({'class': 'btn btn-primary submits'}))


class PasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'Enter new password'})
                             )
    submit = SubmitField('Submit',
                         render_kw=({'class': 'btn btn-primary submits'}))


class WishlistForm(FlaskForm):
    type = SelectField('Item Type',
                       choices=[('book', 'Book'), ('magazine', 'Magazine')],
                       render_kw=({
                           'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                           'id': 'mySelect'}))

    authors = StringField('authors',
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Authors'}))
    title = StringField('title',
                        validators=[DataRequired()],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Title'}))

    pub_date = SelectField('Year of publication',
                           choices=[(str(x), str(x))
                                    for x in
                                    range(1970,
                                          datetime.now().year + 1)],
                           validators=[check_pub_date],
                           render_kw=({
                               'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                               'id': 'mySelect',
                               'placeholder': 'Year of publication'}))

    add = SubmitField('Add new wish',
                      render_kw=({'class': 'btn btn-primary add'}))


class RemoveForm(FlaskForm):
    submit = SubmitField('Delete',
                         render_kw=({'class': 'btn btn-danger btn-sm'}))


class BorrowForm(FlaskForm):
    submit = SubmitField('Borrow',
                         render_kw=({'class': 'btn btn-success submits',
                                     'disabled': False}))


class ReturnForm(FlaskForm):
    submit = SubmitField('Return',
                         render_kw=({'class': 'btn btn-success submits',
                                     'disabled': False}))
