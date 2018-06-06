import re
from wtforms.validators import ValidationError
from init_db import db


def tieto_email(form, field):
    if not re.compile('^[a-z]*\.[a-z-]*@tieto.com$').match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile('^[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid name.')


def surname(form, field):
    if not re.compile('^[A-Z]?[a-z]*-?[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid surname.')

def book_exists(form, field):
    pass