from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import DataRequired, Length
from forms.custom_validators import \
    check_author, check_language, \
    check_category, check_isbn, \
    check_pub_date, title_book_exists


class BookForm(FlaskForm):
    languages = [('polish', 'Polish'),
                 ('english', 'English'),
                 ('other', 'Other')]
    categories = [('developers', 'Developers'),
                  ('managers', 'Managers'),
                  ('magazines', 'Magazines'),
                  ('other', 'Other')]

    # LibraryItem
    title = StringField('Title',
                        validators=[DataRequired(),
                                    Length(3),
                                    title_book_exists],
                        render_kw=({'class': 'inputs',
                                    'placeholder': 'Title'}))

    table_of_contents = TextAreaField('Table of contents',
                                      validators=[DataRequired(),
                                                  Length(3)],
                                      render_kw=({'class': 'inputs',
                                                  'placeholder':
                                                      'Table of contents'}))

    language = SelectField('Language',
                           choices=languages,
                           validators=[check_language],
                           render_kw=({
                               'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                               'id': 'mySelect',
                               'placeholder': 'Language'}))

    category = SelectField('Category',
                           choices=categories,
                           validators=[check_category],
                           render_kw=({
                               'class': 'custom-select mb-2 mr-sm-2 mb-sm-0',
                               'id': 'mySelect',
                               'placeholder': 'Category'}))

    tag = StringField('Tag',
                      validators=[DataRequired(), Length(3)],
                      render_kw=({'class': 'inputs',
                                  'placeholder': 'Tag'}))
    description = TextAreaField('Description',
                                validators=[DataRequired(), Length(3)],
                                render_kw=({'class': 'inputs',
                                            'placeholder': 'Description'}))

    # Book

    isbn = StringField('ISBN number',
                       validators=[DataRequired(), check_isbn],
                       render_kw=({'class': 'inputs',
                                   'placeholder': 'ISBN number'}))

    original_title = StringField('Original title',
                                 validators=[DataRequired(), Length(3)],
                                 render_kw=({'class': 'inputs',
                                             'placeholder': 'Original title'}))
    publisher = StringField('Publisher',
                            validators=[DataRequired()],
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Publisher'}))

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

    # Authors
    first_name = StringField('First name',
                             validators=[check_author],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[check_author],
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Surname'}))

    first_name_1 = StringField('First_name_1',
                               validators=[check_author],
                               render_kw=({'class': 'inputs',
                                           'placeholder': 'First Name 1'}))
    surname_1 = StringField('Surname_1',
                            validators=[check_author],
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Surname 1'}))

    first_name_2 = StringField('First name 2',
                               validators=[check_author],
                               render_kw=({'class': 'inputs',
                                           'placeholder': 'First Name 2'}))
    surname_2 = StringField('Surname 2',
                            validators=[check_author],
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Surname 2'}))

    submit = SubmitField('Create',
                         render_kw=({'class': 'btn btn-primary submits'}))
