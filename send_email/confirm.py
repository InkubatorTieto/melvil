from .emails import send_email
from itsdangerous import URLSafeTimedSerializer
from config import DevConfig
from flask import url_for, render_template


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)

    confirm_url = url_for(
        'library.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)

    html = render_template(
        'registration_email.html',
        confirm_url=confirm_url)

    send_email('Confirm Your Email Address - Tieto library', DevConfig.ADMINS[0], [user_email], None, html)
