import re

from wtforms_alchemy import ModelForm

from wtforms.validators import Regexp

from flask_wtf import FlaskForm

from models import User


email_regex = Regexp('[0-9A-Za-z-.]*@tieto.com$',
                     flags=re.IGNORECASE,
                     message='Insert valid tieto mail.')


class EditProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = User
        only = ['first_name', 'surname', 'email']
        unique_validator = None
        validators = {'email': email_regex}
