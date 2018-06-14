import re

from wtforms.validators import ValidationError
from datetime import datetime
from isbnlib import is_isbn10, is_isbn13
from models.books import Book


def tieto_email(form, field):
    if not re.compile('[0-9A-Za-z-.]*@tieto.com$').match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile('^[A-ZĄĆŚĘŁŃÓŻŹ]{1}[a-ząćęłńśóżź]*$').match(field.data):
        raise ValidationError('Insert valid name.')


def surname(form, field):
    if not re.compile(
            '^[A-ZĄĆŚĘŃŁÓŻŹ]{1}[a-ząćęśłńóżź]*$'
    ).match(field.data) and not \
            re.compile('^[A-ZĄĆŚĘŃŁÓŻŹ]{1}[a-ząćęśłńóżź]*'
                       '-?[A-ZĄĆĘŃŁÓŻŹ]?[a-ząćęłśńóżź]*$').match(field.data) \
            and not re.compile('^[A-ZĄĆŚĘŃŁÓŻŹ]{1}[a-ząćęśłńóżź]*'
                               '\s?[A-ZĄĆĘŃŁÓŻŹ]?[a-ząćęłśńóżź]*$').match(field.data):
        raise ValidationError('Insert valid surname.')


def check_password(form, field):
    if len(field.data) < 8:
        ValidationError("Make sure your password is at lest 8 letters")
    if re.search('[0-9]+', field.data) is None:
        raise ValidationError("Make sure your password has a number in it")
    if re.search("[A-ZĄĆŚĘŃŁÓŻŹ]+", field.data) is None:
        raise ValidationError("Make sure your password has a capital letter in it")
    if re.search("[!#@\$%^&*()_]+", field.data) is None:
        raise ValidationError("Make sure your password has a special character in it, for example: '! @ #'")
    if re.search("[\.\,]+", field.data) is not None:
        raise ValidationError("Your has a dot or comma, these characters are not allowed")


def check_author(form, field):
    if field.data != '':
        if not re.compile('^([A-ZĄŚĆĘŁŃÓŻŹ]{1}.*[A-ZĄĆŚŃĘŁÓŻŹa-ząćęłśóńżź]*'
                          '[a-ząćęłśóżńź])$').match(field.data) and \
                not re.compile('^[A-ZŚĄĆŃĘŁÓŻŹ]{1}.'
                               '[A-ZĄĆŚĘŃŁÓŻŹ]$').match(field.data) or \
                re.compile('^[a-ząćęńśłóżź]*$').match(field.data):
            raise ValidationError('Insert valid author name or surname.')


def check_language(form, field):
    languages = ['polish', 'english', 'other']
    if field.data not in languages:
        raise ValidationError('Language is unavailable. Select correct!')


def check_category(form, field):
    categories = ['developers', 'managers', 'magazines', 'other']
    if field.data not in categories:
        raise ValidationError('This category is unavailable. Select correct!')


def check_isbn(form, field):
    field.data = field.data.replace("-", "").replace(" ", "")
    if not is_isbn10(field.data) and not is_isbn13(field.data):
        raise ValidationError('ISBN number is incorrect!')

    if Book.query.filter_by(isbn=field.data).first():
        raise ValidationError('This book is already in the database.')


def check_pub_date(form, field):
    if int(field.data) > datetime.now().year:
        raise ValidationError('Date is incorrect.')

    if int(field.data) < 1970:
        raise ValidationError('Date is incorrect.')

    if type(field.data) != str:
        raise ValidationError('Type of data is incorrect')


def title_book_exists(form, field):
    results = Book.query.filter(Book.title.startswith(field.data[:2])).all()
    for i in results:
        i = str(i.title)
        i = i.replace(" ", "").replace("_", "") \
            .replace("-", "").replace(",", ""). \
            replace(".", "").lower()
        tmp = str(field.data)
        tmp = tmp.replace(" ", "").replace("_", ""). \
            replace("-", "").replace(",", "") \
            .replace(".", "").lower()
        if i == tmp:
            raise ValidationError('This book already exists.'
                                  ' This title is in database!')
