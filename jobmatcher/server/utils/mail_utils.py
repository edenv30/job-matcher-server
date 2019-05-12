from mimetypes import MimeTypes

from jobmatcher.config import config
from flask import current_app
from flask_mail import Message


def send_mail(subject, recipients, body=None, html=None, attachments=[]):
    mail = current_app.extensions['mail']
    msg = Message(sender=config.MAIL_SENDER, subject=subject, recipients=recipients, html=html, body=body)
    mimes = MimeTypes()
    for file in attachments:
        path_ = file
        with current_app.open_resource(path_) as fp:
            mime = mimes.guess_type(fp.name)
            msg.attach(path_, mime[0], fp.read())
    mail.send(msg)
