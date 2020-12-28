from model import db, Receipt, cardEvents, userEvents, ReceiptPdf
from FileEvents import createpdfdata, savepdf
from dateFunction import getdate


def viewall(): return Receipt.query.all()


def view(id): return Receipt.query.get(id)


# receiptEvents.add(senderid=1, receiverid=2, amount=1000, detail="sıcakyemek.tech adresinde 10 TL harcama yapıldı.")
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
        adddbfile(senderid=senderid, detail=detail, amount=amount, receiptid=newreceipt.id)

        # todo Send Mail // atachment to pdf

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
    data = {
        "cardnumber": hidecardnumber(carnumber=cardEvents.viewuser(userid=senderid).cardnumber),
        "processdate": getdate(),
        "processdetail": detail,
        "amount": userEvents.amountformatter(amount)
    }
    pdfdata = createpdfdata(data=data)

    newreceiptpdf = ReceiptPdf(
        receiptid=receiptid,
        pdf=pdfdata
    )
    db.session.add(newreceiptpdf)
    db.session.commit()
    db.session.rollback()

    savepdf(pdfdata=pdfdata, receiptid=receiptid)
    return True


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





