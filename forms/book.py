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
    # pole do daty do daty tutaj zakomentowałem w celach testu itp ale dalej i tak nie działa
    
    pub_date = DateField('Date of publication',
                         render_kw=({'class': "dtpick",
                                         'placeholder': "DD/MM/YYYY"
                                      }))
                         # id="dtpick")
    # validators=[DataRequired()], render_kw = ({'placeholder': "DD/MM/YYYY"
                  # })



    # AUTORZY
    first_name = StringField('First name',
                             validators=[Length(3), name],
                             render_kw=({'class': 'inputs',
                                         'placeholder': 'First Name'}))
    surname = StringField('Surname',
                          validators=[Length(3), surname],
                          render_kw=({'class': 'inputs',
                                      'placeholder': 'Surname'}))

    submit = SubmitField('Create',
                         render_kw=({'class': 'btn btn-primary submits'}))
