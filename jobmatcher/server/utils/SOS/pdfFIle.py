import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def convertHtmlToDfdFile(urlFile):
    print('convertHtmlToDfdFile')
    pdf = pdfkit.from_url(urlFile, False)
    msg = MIMEMultipart()
    msg.attach(pdf)
    # fromaddr = "chenyair1617@gmail.com"
    # toaddr = "chenyair1617@gmail.com"
    # mailer = smtplib.SMTP()
    # mailer.connect()
    # mailer.sendmail(fromaddr, toaddr, msg.as_string())
    # mailer.close()

    # fromaddr = "chenyair1617@gmail.com"
    # toaddr = "chenyair1617@gmail.com"
    # # instance of MIMEMultipart
    # msg = MIMEMultipart()
    # # storing the senders email address
    # msg['From'] = fromaddr
    # # storing the receivers email address
    # msg['To'] = toaddr
    # # storing the subject
    # msg['Subject'] = "Subject of the Mail"
    # # string to store the body of the mail
    # body = "Body_of_the_mail"
    # # attach the body with the msg instance
    # msg.attach(MIMEText(body, 'plain'))
    #
    # # open the file to be sent
    # filename = "shaurya"
    # attachment = open("C:\\Users\\cheny\\PycharmProjects\\server\\job-matcher-server\\jobmatcher\\server\\shaurya.pdf", "rb")
    #
    # # instance of MIMEBase and named as p
    # p = MIMEBase('application', 'octet-stream')
    #
    # # To change the payload into encoded form
    # p.set_payload((attachment).read())
    #
    # # encode into base64
    # encoders.encode_base64(p)
    #
    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #
    # # attach the instance 'p' to instance 'msg'
    # msg.attach(p)
    #
    # # creates SMTP session
    # s = smtplib.SMTP('smtp.gmail.com', 587)
    #
    # # start TLS for security
    # s.starttls()
    #
    # # Authentication
    # s.login(fromaddr, "Password_of_the_sender")
    #
    # # Converts the Multipart msg into a string
    # text = msg.as_string()
    #
    # # sending the mail
    # s.sendmail(fromaddr, toaddr, text)
    #
    # # terminating the session
    # s.quit()


    # print(pdf)
