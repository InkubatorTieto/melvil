from flask_mail import Message
from threading import Thread


def send_async_email(app, msg):
    from app import mail
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    from app import create_app
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[create_app(), msg])
    thr.start()

