import os
import smtplib
import pdfkit

from jobmatcher.config import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jobmatcher.server.modules.job.job import Job
from jobmatcher.server.utils.mail_utils import send_mail


def makeJobHtml(job):
    return """
        <div>
            <div>Description %s</div>
        </div>
    """ % (job.description)

def makeUserInfoHtml(user):
    return """
        <div>%s</div>
    """ % (user.fullname)

def makeUserJobsPdf(user):
    jobs = Job.objects.filter(identifier__in=(user.jobs.keys()))

    html = """
        <html>
            <head>
                <meta http-equiv="content-type" content="text/html"; charset="utf-8">
            </head>
            <body>
                %s
                <div>%s</div>
            </body>
        </html>
    """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in jobs]))

    output_filename = 'temp.pdf'
    options = {'quiet': ''}
    pdfkit.from_string(html, output_filename, css=['%s/utils/SOS/pdfFileStyle.css' % os.getcwd()], options=options)
    subject = 'Your Job Matches'
    body = 'Your Job Matches'

    send_mail(subject, [user.email], body=body, html=None, attachments=['%s/%s' % (os.getcwd(), output_filename)])

def convertHtmlToDfdFile(urlFile,receiver,subject,message):
    msg = MIMEMultipart()
    msg['From'] = config.MAIL_SENDER
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = subject+".pdf"
    attachment = pdfkit.from_url(urlFile,False)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)


    server = smtplib.SMTP_SSL(config.MAIL_SERVER,config.MAIL_PORT)
    # server.starttls()
    server.login(config.MAIL_SENDER, config.MAIL_PASSWORD)
    text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(config.MAIL_SENDER, receiver, text)
    server.quit()

