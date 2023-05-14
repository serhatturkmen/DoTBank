from model import db, Receipt, cardEvents, userEvents, ReceiptPdf
from FileEvents import createpdfdata, savepdf, sendmail
from dateFunction import getdate


def viewall(): return Receipt.query.all()


def view(id): return Receipt.query.get(id)


def add(senderid, receiverid, amount, detail):
    try:
        newreceipt = Receipt(
            senderid=senderid,
            receiverid=receiverid,
            amount=amount,
            detail=detail
        )
        db.session.add(newreceipt)
        db.session.commit()
        db.session.rollback()

        # Save to Pdf File on Database
        pdfdata = adddbfile(senderid=senderid, detail=detail,
                  amount=amount, receiptid=newreceipt.id)
        if pdfdata:
            senderdata = userEvents.view(id=senderid)
            sendmail(
                sendmailadress=senderdata.email,
                subject="DoTBank İşlem Dekontu",
                body=detail,
                receiptdata=pdfdata
            )
        return True
    except Exception as e:
        print("Dekont eklenemedi.")
        print("Dekont Bilgileri.")
        print("Senderid = "+str(senderid))
        print("Receiverid = "+str(receiverid))
        print("Amount = "+str(amount))
        print("Detail = "+detail)
        print("Hata:::")
        print(str(e))
        return False


def adddbfile(senderid, detail, amount, receiptid):
    try:
        data = {
            "cardnumber": hidecardnumber(carnumber=cardEvents.viewuser(userid=senderid).cardnumber),
            "processdate": getdate(),
            "processdetail": detail,
            "amount": amount
        }
        pdfdata = createpdfdata(data)

        # save pdf on database
        newreceiptpdf = ReceiptPdf(
            receiptid=receiptid,
            pdf=pdfdata
        )
        db.session.add(newreceiptpdf)
        db.session.commit()
        db.session.rollback()

        # add local file
        savepdf(pdfdata=pdfdata, receiptid=receiptid)

        return pdfdata
    except Exception as e:
        print(str(e))
        return False


def delete(id):
    try:
        data = view(id)
        db.session.delete(data)
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Dekont silmede hata alındı.")
        print("Hata:::")
        print(str(e))
        return False


def hidecardnumber(carnumber):
    return carnumber[0] + carnumber[1] + carnumber[2] + carnumber[3] + "********" + carnumber[12] + carnumber[13] + carnumber[14] + carnumber[15]


def get_receipt_pdf(receipt_id):
    receipt = view(receipt_id)
    data = {
        "cardnumber": hidecardnumber(carnumber=cardEvents.viewuser(userid=receipt.senderid).cardnumber),
        "processdate": receipt.processdate,
        "processdetail": receipt.detail,
        "amount": receipt.amount
    }
    data = createpdfdata(data)
    return data
