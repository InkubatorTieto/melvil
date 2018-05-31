from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from forms.custom_validators import tieto_email, name, surname


class BookForm(FlaskForm):

    leanguages = [('polish', 'Polish'), ('english', 'English'), ('other', 'Other')]
    categories = [('developers', 'Developers'),
                  ('managers', 'Managers'),
                  ('magazines', 'magazines'),
                  ('other', 'Other')]

    # LibraryItem
    title = StringField('Title',
                        validators=[DataRequired(), Length(3), name],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Title'}))

    table_of_contents = StringField('Table of contents',
                        validators=[DataRequired(), Length(3), name],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Table of contents'}))

    leanguage = SelectField('Leanguage',
                                    choices=leanguages,
                                    render_kw=({'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                                                'id': 'mySelect',
                                                'placeholder': 'Leanguage'}))

    category = SelectField('Category',
                            choices=categories,
                            render_kw=({'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                                        'id': 'mySelect',
                                        'placeholder': 'Category'}))

    tag = StringField('Tag',
                        validators=[DataRequired(), Length(3), name],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Tag'}))
    description = StringField('Description',
                        validators=[DataRequired(), Length(3), name],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Description'}))

    # Book

    isbn = StringField('ISBN number',
                       validators=[DataRequired()],
                       render_kw=({'class': 'inputs',
                                   'placeholder': 'ISBN number'}))

    original_title = StringField('Original title',
                             validators=[DataRequired(), Length(3), name],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'Original title'}))
    publisher = StringField('Publisher',
                       validators=[DataRequired()],
                       render_kw=({'class': 'inputs',
                                   'placeholder': 'Publisher'}))

    pub_date = DateField('Date',
                            format='%Y-%m-%d',
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Publisher'}))

    # AUTORZY
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(3), name],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[DataRequired(), Length(3), surname],
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Surname'}))

    # submit = SubmitField('Sign In',
    #                      render_kw=({'class': 'btn btn-primary submits'}))