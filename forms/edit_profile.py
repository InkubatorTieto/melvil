from wtforms import StringField, PasswordField, SubmitField
from wtforms_alchemy import ModelForm


from flask_wtf import FlaskForm

from models import User


class EditProfileForm(ModelForm, FlaskForm):
    class Meta:
        model = User



# class EditProfileForm(FlaskForm):
#         email = StringField('Email', validators=)
#         first_name = StringField('First name')
#         surname = StringField('Surname')
#         password = PasswordField('Password')
#         submit = SubmitField('Confirm')
