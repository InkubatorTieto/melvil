from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField,
    FieldList,
    FormField
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

    table_of_contents = TextAreaField('Table of contents',
                                      validators=[DataRequired(), Length(3)],
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
    description = TextAreaField('Description',
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

    pub_date = DateField('Date of publication',
                         format='%d/%m/%Y',
                         render_kw=({'class': "dtpick",
                                     'placeholder': "DD/MM/YYYY"
                                     }))
    # AUTORZY
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(3), name],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[DataRequired(), Length(3), surname],
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Surname'}))

    first_name_1 = StringField('First_name_1',
                               validators=[],
                               render_kw=({'class': 'inputs',
                                           'placeholder': 'First Name 1'}))
    surname_1 = StringField('Surname_1',
                            validators=[],
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Surname 1'}))

    first_name_2 = StringField('First name 2',
                               validators=[],
                               render_kw=({'class': 'inputs',
                                           'placeholder': 'First Name 2'}))
    surname_2 = StringField('Surname 2',
                            validators=[],
                            render_kw=({'class': 'inputs',
                                        'placeholder': 'Surname 2'}))

    submit = SubmitField('Create',
                         render_kw=({'class': 'btn btn-primary submits'}))
