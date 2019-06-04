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

# def makeUserJobsPdf(user):
#     print("******* makeUserJobsPdf() *********")
#     jobs = Job.objects.filter(identifier__in=(user.jobs.keys()))
#     print("user_mail: " + user.email)
#     # print("jobs: ", jobs)
#
#     html = """
#         <html>
#             <head>
#                 <meta http-equiv="content-type" content="text/html"; charset="utf-8">
#             </head>
#             <body>
#                 <div class="content">
#                     <div class="user-info">%s</div>
#                     <div class="user-matches">%s</div>
#                 </div>
#             </body>
#         </html>
#     """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in jobs]))
#
#     output_filename = 'temp.pdf'
#     options = {'quiet': ''}
#     pdfkit.from_string(html, output_filename, css=['%s/utils/SOS/pdfFileStyle.css' % os.getcwd()], options=options)
#
#     subject = 'Your Job Matches'
#     body = 'Your Job Matches'
#     send_mail(subject, [user.email], body=body, html=None, attachments=['%s/%s' % (os.getcwd(), output_filename)])


def html_sending(user):
    keys = list()
    items = user.sending.items()
    for item in items:
        if item[1]:
            keys.append(item[0])

    send = Job.objects.filter(identifier__in=keys)

    html = """
                <html>
                    <head>
                        <meta http-equiv="content-type" content="text/html"; charset="utf-8">
                    </head>
                    <body>
                        <div class="logo">
                            <h1 class="logo-title">Job Matcher</h1>
                            <h2 class="type-title">Sending jobs matches</h2>
                        </div>
                        <br/>
                        <br/>
                        <div class="content">
                            <div class="user-info">%s</div>
                            <div class="user-matches">%s</div>
                        </div>
                    </body>
                </html>
            """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in send]))

    return html


def html_jobs(user):
    jobs = Job.objects.filter(identifier__in=(user.jobs.keys()))

    html = """
                <html>
                    <head>
                        <meta http-equiv="content-type" content="text/html"; charset="utf-8">
                    </head>
                    <body>
                        <div class="logo">
                            <h1 class="logo-title">Job Matcher</h1>
                            <h2 class="type-title">Jobs matches</h2>
                        </div>
                        <br/>
                        <br/>
                        <div class="content">
                            <div class="user-info">%s</div>
                            <div class="user-matches">%s</div>
                        </div>
                    </body>
                </html>
            """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in jobs]))

    return html


def html_reply(user):
    keys = list()
    items = user.replay.items()
    for item in items:
        if item[1]:
            keys.append(item[0])
    reply = Job.objects.filter(identifier__in=keys)

    html = """
                <html>
                    <head>
                        <meta http-equiv="content-type" content="text/html"; charset="utf-8">
                    </head>
                    <body>
                        <div class="logo">
                            <h1 class="logo-title">Job Matcher</h1>
                            <h2 class="type-title">Reply jobs matches</h2>
                        </div>
                        <br/>
                        <br/>
                        <div class="content">
                            <div class="user-info">%s</div>
                            <div class="user-matches">%s</div>
                        </div>
                    </body>
                </html>
            """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in reply]))

    return html


def html_favorite(user):
    keys = list()
    items = user.favorite.items()
    for item in items:
        if item[1]:
            keys.append(item[0])
    favorite = Job.objects.filter(identifier__in=keys)

    html = """
                    <html>
                        <head>
                            <meta http-equiv="content-type" content="text/html"; charset="utf-8">
                        </head>
                        <body>
                            <div class="logo">
                                <h1 class="logo-title">Job Matcher</h1>
                                <h2 class="type-title">Favorite jobs matches</h2>
                            </div>
                            <br/>
                            <br/>
                            <div class="content">
                                <div class="user-info">%s</div>
                                <div class="user-matches">%s</div>
                            </div>
                        </body>
                    </html>
                """ % (makeUserInfoHtml(user), ''.join([makeJobHtml(job) for job in favorite]))

    return html


# TODO: add to func - try&catch later
def send_user_mail(user, selected_filter):
    if selected_filter == 'showAll':
        current_html = html_jobs(user)
    elif selected_filter == 'favorite':
        current_html = html_favorite(user)
    elif selected_filter == 'sending':
        current_html = html_sending(user)
    elif selected_filter == 'reply':
        current_html = html_reply(user)
    else:
        current_html = html_jobs(user)

    fromaddr = config.MAIL_SENDER
    toaddr = user.email

    msg = MIMEMultipart()

    msg['To'] = toaddr
    msg['Subject'] = "Your job match results"
    msg['From'] = fromaddr
    body = 'Your Job Matches'
    msg.attach(MIMEText(body, 'plain'))

    output_filename = 'temp.pdf'
    options = {'quiet': ''}
    pdfkit.from_string(current_html, output_filename, css=['%s/utils/SOS/pdfFileStyle.css' % os.getcwd()], options=options)

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




