from itsdangerous import URLSafeTimedSerializer

from flask import url_for, render_template

from config import DevConfig
from .emails import send_email


def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)

    confirm_url = url_for(
        "library.confirm_email",
        token=confirm_serializer.dumps(
            user_email, salt="email-confirmation-salt"
        ),
        _external=True,
    )

    html = render_template("registration_email.html", confirm_url=confirm_url)
    body = html

    send_email(
        "Confirm Your Email Address - Tieto library",
        DevConfig.ADMINS[0],
        [user_email],
        None,
        body,
    )


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(DevConfig.SECRET_KEY)

    password_reset_url = url_for(
        "library.reset_with_token",
        token=password_reset_serializer.dumps(
            user_email, salt="password-reset-salt"
        ),
        _external=True,
    )

    html = render_template(
        "password_reset_email.html", password_reset_url=password_reset_url
    )

    send_email(
        "Password Reset Requested",
        DevConfig.ADMINS[0],
        [user_email],
        None,
        html,
    )
