# -*- coding: utf-8 -*-
import re
from wtforms.validators import ValidationError


def tieto_email(form, field):
    if not re.compile('[0-9A-Za-z-.]*@tieto.com$').match(field.data):
        raise ValidationError('Only Tieto emails are accepted.')


def name(form, field):
    if not re.compile('^[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*$').match(field.data):
        raise ValidationError('Insert valid name.')


def surname(form, field):
    if not re.compile(
            '^[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*-?[A-ZĄĆĘŁÓŻŹ]?[a-ząćęłóżź]*$'
            ).match(field.data):
        raise ValidationError('Insert valid surname.')
