from model import db, Card


def viewall(): return Card.query.all()


def view(id): return Card.query.get(id)


def viewuser(userid): return Card.query.filter_by(userid=userid).first()


def trust(cardnumber, year, month, secretkey, name):
    try:
        card = Card.query.filter_by(cardnumber=cardnumber).first()
        if card.name == name and card.year == int(year) and card.month == int(month) and card.secretkey == int(secretkey):
            return card.id
        else:
            return False
    except Exception as e:
        print("Kart bilgileri doğrulamada hata alındı.")
        print("Hata:")
        print(str(e))
        return False


def add(cardnumber, year, month, secretkey, name, userid):
    try:
        newcard = Card(
            cardnumber=cardnumber,
            year=year,
            month=month,
            secretkey=secretkey,
            name=name,
            userid=userid
        )
        db.session.add(newcard)
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Kart eklemede hata alındı.")
        print("Hata:")
        print(str(e))
        return False


def delete(id):
    try:
        newcard = view(id=id)
        db.session.delete(newcard)
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Kart silmede hata alındı.")
        print("Hata:")
        print(str(e))
        return False
