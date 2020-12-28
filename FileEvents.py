from flask import render_template
from dateFunction import getdate
from flask_weasyprint import render_pdf, HTML
import os


def createpdfdata(data):
    html = render_template("receiptpdftemplate.html", data=data)
    return render_pdf(HTML(string=html)).data


def savepdf(pdfdata, receiptid):
    # save a file
    if not os.path.exists(path="receipts"):
        os.mkdir("receipts")
    pdffile = open("receipts/receipt-"+str(receiptid)+" -"+getdate()+".pdf", 'wb')
    pdffile.write(pdfdata)
    pdffile.close()
