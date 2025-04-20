from flask import render_template
from dateFunction import getdate
from flask_weasyprint import render_pdf, HTML
import os
from flask import current_app as app

# mail için
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

from email.mime.base import MIMEBase
from email import encoders


def createpdfdata(data):
    html = render_template("receiptpdftemplate.html", data=data)
    return HTML(string=html).write_pdf()


def savepdf(pdfdata, receiptid):
    try:
        # save a file
        if not os.path.exists(path="receipts"):
            os.mkdir("receipts")
        filepath =os.path.join(app.root_path, 'receipts', "receipt-" + str(receiptid) + ".pdf")
        pdffile = open(filepath, 'wb')
        pdffile.write(pdfdata)
        pdffile.close()
    except Exception as e:
        print(str(e))


def sendmail(sendmailadress, subject, body, receiptdata, inhtml=True):
    mailadress = os.getenv("EMAIL_USERNAME")
    mailpass = os.getenv("EMAIL_PASSWORD")
    mailserver = os.getenv("EMAIL_SERVER")
    mailport = 587
    if mailadress == sendmailadress:
        return 2
    message = MIMEMultipart()
    message["From"] = mailadress
    message["To"] = sendmailadress
    message["Subject"] = subject
    body = body
    if inhtml:
        body_text = MIMEText(body, "html")
    else:
        body_text = MIMEText(body, "plain")
    message.attach(body_text)

    if receiptdata:
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(receiptdata)
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment; filename="receipt.pdf"')
        message.attach(payload)

    try:
        mail = smtplib.SMTP(host=mailserver, port=mailport)
        mail.ehlo()
        mail.starttls()
        mail.login(mailadress, mailpass)
        mail.sendmail(message["From"], message["To"], message.as_string())
        result = 1
        mail.close()
    except Exception as e:
        print("Mail gönderiminde bir hata alındı. Hata metni:")
        print(str(e))
        result = 3
    return result
