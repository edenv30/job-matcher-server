import smtplib
import pdfkit
from jobmatcher.config import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def convertHtmlToDfdFile(urlFile,receiver,subject,message):

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


    server = smtplib.SMTP(config.MAIL_SERVER)
    server.starttls()
    server.login(config.MAIL_SENDER, config.MAIL_PASSWORD)
    text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(config.MAIL_SENDER, receiver, text)
    server.quit()

