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
        <div class="user-match">
            <div>Role: %s</div>
            <div>Location: %s</div>
            <div>Description: %s</div>
            <br/>
        </div>
    """ % (job.role_name, job.location ,job.description)

def makeUserInfoHtml(user):
    return """
        <div><u>%s</u></div><br/>
    """ % (user.fullname)

def makeUserJobsPdf(user):
    print("******* makeUserJobsPdf() *********")
    jobs = Job.objects.filter(identifier__in=(user.jobs.keys()))
    print("user_mail: " + user.email)
    # print("jobs: ", jobs)

    html = """
        <html>
            <head>
                <meta http-equiv="content-type" content="text/html"; charset="utf-8">
            </head>
            <body>
                <div class="content">
                    <div class="user-info">%s</div>
                    <div class="user-matches">%s</div>
                </div>
            </body>
        </html>
    """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in jobs]))

    output_filename = 'temp.pdf'
    options = {'quiet': ''}
    pdfkit.from_string(html, output_filename, css=['%s/utils/SOS/pdfFileStyle.css' % os.getcwd()], options=options)

    subject = 'Your Job Matches'
    body = 'Your Job Matches'
    send_mail(subject, [user.email], body=body, html=None, attachments=['%s/%s' % (os.getcwd(), output_filename)])


# TODO: add to func - try&catch later
def send_user_mail(user):
    print("####### mail_test() #####")
    jobs = Job.objects.filter(identifier__in=(user.jobs.keys()))

    fromaddr = config.MAIL_SENDER
    toaddr = user.email

    msg = MIMEMultipart()

    msg['To'] = toaddr
    msg['Subject'] = "Your job match results"
    msg['From'] = fromaddr
    body = 'Your Job Matches'
    msg.attach(MIMEText(body, 'plain'))

    html = """
            <html>
                <head>
                    <meta http-equiv="content-type" content="text/html"; charset="utf-8">
                </head>
                <body>
                    <div class="content">
                        <div class="user-info">%s</div>
                        <div class="user-matches">%s</div>
                    </div>
                </body>
            </html>
        """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in jobs]))

    output_filename = 'temp.pdf'
    options = {'quiet': ''}
    pdfkit.from_string(html, output_filename, css=['%s/utils/SOS/pdfFileStyle.css' % os.getcwd()], options=options)

    filename = "temp.pdf"
    attachment = open('temp.pdf', "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    server = smtplib.SMTP_SSL(config.MAIL_SERVER, config.MAIL_PORT)
    server.login(config.MAIL_SENDER, config.MAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    # close the attachment and remove the file
    attachment.close()
    os.remove("temp.pdf")















def convertHtmlToDfdFile(urlFile,receiver,subject,message):
    print(" ****** convertHtmlToDfdFile ******")
    msg = MIMEMultipart()
    msg['From'] = config.MAIL_SENDER
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = subject+".pdf"
    attachment = pdfkit.from_url(urlFile, False)
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

