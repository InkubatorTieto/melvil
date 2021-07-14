from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm

from models import Copy


class CopyAddForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy


class CopyEditForm(ModelForm, FlaskForm):
    class Meta:
        model = Copy
        unique_validator = None
