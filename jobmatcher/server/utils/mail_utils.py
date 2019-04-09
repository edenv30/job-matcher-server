from jobmatcher.config import config
from flask import current_app
from flask_mail import Message


def send_mail(subject, recipients, body=None, html=None):
    mail = current_app.extensions['mail']
    msg = Message(sender=config.MAIL_SENDER, subject=subject, recipients=recipients, html=html, body=body)
    mail.send(msg)
