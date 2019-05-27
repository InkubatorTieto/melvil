import re

from wtforms.validators import Regexp
from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm

from models import Copy

""" Regex return True for assets like "ab123456" or "123456".
General template:
two letters (letter case does not matter) + six digits
or six digits only
"""
asset_code_regex = Regexp('^([A-Z]{2}[0-9]{6}|[0-9]{6})$',
                          flags=re.IGNORECASE,
                          message='Insert valid asset code eg. ab123456 or 123456')


class CopyAddForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy
        validators = {'asset_code': asset_code_regex}


class CopyEditForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy
        unique_validator = None
        validators = {'asset_code': asset_code_regex}
