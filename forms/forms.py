from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired

from forms.custom_validators import check_pub_date, tieto_email


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()],
        render_kw=({'class': 'inputs', 'placeholder': 'Username'})
    )
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'Password'}))
    remember_me = BooleanField(label='Remember Me')

    submit = SubmitField('Sign In',
                         render_kw=({'class': 'btn btn-primary submits'}))


class ContactFormLogin(FlaskForm):
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


class ContactFormNoLogin(ContactFormLogin):
    email = StringField('email',
                        validators=[tieto_email],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Email'}))


class SearchForm(FlaskForm):
    query = StringField('Search',
                        render_kw=({'class': 'inputs',
                                    'type': 'text',
                                    'placeholder': 'Search...'}))


class WishlistForm(FlaskForm):
    type = SelectField('Item Type',
                       choices=[('book', 'Book'), ('magazine', 'Magazine')],
                       render_kw=({
                           'class': 'inputs custom-select'
                                    ' mb-2 mr-sm-2 mb-sm-0',
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
                               'class': 'inputs custom-select'
                                        ' mb-2 mr-sm-2 mb-sm-0',
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
