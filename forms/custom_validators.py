import re
from wtforms.validators import ValidationError
from datetime import datetime
from isbnlib import is_isbn10, is_isbn13
from models.books import Book


def tieto_email(form, field):
    if not re.compile('^[a-z]*\.[a-z-]*@tieto.com$').match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile('^[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid name.')


def surname(form, field):
    if not re.compile('^[A-Z]?[a-z]*-?\s*[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid surname.')


def check_author(form, field):
    if field.data != '':
        if not re.compile('^[A-Z]?.*[a-z]*[A-Za-z]$').match(field.data):
            raise ValidationError('Insert valid author name or surname.')


def check_language(form, field):
    languages = ['polish', 'english','other']
    if field.data not in languages:
        raise ValidationError('Language is unavailable. Select correct!')


def check_category(form, field):
    categories = ['developers', 'managers', 'magazines', 'other']
    if field.data not in categories:
        raise ValidationError('This category is unavailable. Select correct!')


def check_isbn(form, field):
    if not is_isbn10(field.data) and not is_isbn13(field.data):
        raise ValidationError('ISBN number is incorrect!')

    if Book.query.filter_by(isbn=field.data).first():
        raise ValidationError('This book is already in the database.')


def check_pub_date(form,field):
    if int(field.data) > datetime.now().year:
        raise ValidationError('Date is incorrect.')

    if int(field.data) < 1970:
        raise ValidationError('Date is incorrect.')

    if type(field.data) != int and type(field.data) != str:
        raise ValidationError('Type of data is incorrect')


def book_exists(form):
    pass
