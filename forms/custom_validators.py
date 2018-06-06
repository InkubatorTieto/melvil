import re
from wtforms.validators import ValidationError


def tieto_email(form, field):
    if not re.compile('^[a-z]*\.[a-z-]*@tieto.com$').match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile('^[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid name.')


def surname(form, field):
    if not re.compile('^[A-Z]?[a-z]*-?[A-Z]?[a-z]*$').match(field.data):
        raise ValidationError('Insert valid surname.')


#def pub_date(form, field):
#    if not re.compile('[0-9]').match(field.data):
#        raise ValidationError('Insert valid date.')