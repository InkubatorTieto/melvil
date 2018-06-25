import re

from wtforms_alchemy import ModelForm
from wtforms.validators import Regexp
from flask_wtf import FlaskForm

from models import User
from forms.custom_validators import email_regex


tieto_mail_regex = Regexp(email_regex(),
                          flags=re.IGNORECASE,
                          message='Insert valid tieto mail.')


class EditProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = User
        only = ['first_name', 'surname', 'email']
        unique_validator = None
        validators = {'email': tieto_mail_regex}
