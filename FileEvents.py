from flask import render_template
from dateFunction import getdate
from flask_weasyprint import render_pdf, HTML
import os

# mail için
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys


def createpdfdata(data):
    html = render_template("receiptpdftemplate.html", data=data)
    return render_pdf(HTML(string=html)).data


def savepdf(pdfdata, receiptid):
    try:
        # save a file
        if not os.path.exists(path="receipts"):
            os.mkdir("receipts")
        pdffile = open("receipts/receipt-"+str(receiptid) +
                    "-"+getdate()+".pdf", 'wb')
        pdffile.write(pdfdata)
        pdffile.close()
    except Exception as e:
        print(str(e))


def sendmail(sendmailadress, subject, body, inhtml=True):
    mailadress = "mailinformation.smtpEmail"
    mailpass = "mailinformation.smtpPassword"
    mailserver = "mailinformation.smtpServer"
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
    message.attach
    try:
        mail = smtplib.SMTP(host=mailserver, port=mailport)
        mail.ehlo()
        mail.starttls()
        mail.login(mailadress, mailpass)
        mail.sendmail(message["From"], message["To"], message.as_string())
        result = 1
        mail.close()
    except Exception as e:
        print("Mail ... Bir hata oluştu. Tekrar deneyin...")
        print(str(e))
        result = 3
    return result
