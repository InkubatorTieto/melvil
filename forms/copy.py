from wtforms_alchemy import ModelForm

from models import Copy


class CopyForm(ModelForm):
    class Meta:
        model = Copy
