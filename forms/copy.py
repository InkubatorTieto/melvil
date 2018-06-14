import re

from wtforms.validators import Regexp
from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm

from models import Copy

asset_code_regex = Regexp('^[A-Z]{2}[0-9]{6}$',
                          flags=re.IGNORECASE,
                          message='Insert valid asset code.')


class CopyAddForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy
        validators = {'asset_code': asset_code_regex}


class CopyEditForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy
        unique_validator = None
        validators = {'asset_code': asset_code_regex}
