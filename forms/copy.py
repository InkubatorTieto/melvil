import re

from wtforms.validators import Regexp
from wtforms_alchemy import ModelForm

from models import Copy


class CopyForm(ModelForm):
    class Meta:
        model = Copy
        validators = {'asset_code': Regexp('^[A-Z]{2}[0-9]{6}$',
                                           flags=re.IGNORECASE,
                                           message='Insert valid asset code.')}
