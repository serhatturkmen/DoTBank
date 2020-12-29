from model import db, User, receiptEvents


def viewall(): return User.query.all()


def view(id): return User.query.get(id)


def getamount(userid): return User.query.get(userid).amount


def add(name, surname, email, amount=0):
    try:
        newuser = User(
            name=name,
            surname=surname,
            email=email,
            amount=amount
        )
        db.session.add(newuser)
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Kullanıcı eklemede hata alındı.")
        print("Hata:::")
        print(str(e))
        return False


def update(id, name, surname, email):
    try:
        updateuser = view(id=id)
        updateuser.name = name,
        updateuser.surname = surname,
        updateuser.email = email
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Kullanıcı eklemede hata alındı.")
        print("Hata:::")
        print(str(e))
        return False


def delete(userid):
    try:
        user = view(userid)
        db.session.delete(user)
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Para yatırmada hata alındı.")
        print("Hata:")
        print(str(e))
        return False


#para yatırma
def deposit(userid, quantity):
    try:
        user = view(userid)
        if not user:
            return False
        user.amount = user.amount + quantity
        db.session.commit()
        db.session.rollback()
        return True
    except Exception as e:
        print("Para yatırmada hata alındı.")
        print("Hata:")
        print(str(e))
        return False


#para çekme
def withdraw(userid, quantity):
    try:
        user = view(userid)
        if not user:
            return False
        if user.amount >= quantity:
            user.amount = user.amount - quantity
            db.session.commit()
            db.session.rollback()
            return True
        return False
    except Exception as e:
        print("Para çekmede hata alındı.")
        print("Hata:")
        print(str(e))
        return False


def amountformatter(amount):
    stramount = str(amount)
    if len(stramount) < 3:
        return "0," + stramount[len(stramount) - 2] + "" + stramount[len(stramount) - 1]
    return stramount[0:len(stramount)-2]+"," + stramount[len(stramount)-2] + "" + stramount[len(stramount)-1]


def sendmoney(senderid, receiverid, amount, detail):
    if withdraw(senderid, amount):
        if deposit(receiverid, amount):
            addreceipt = receiptEvents.add(
                senderid=senderid,
                receiverid=receiverid,
                amount=amount,
                detail=detail
            )
            if addreceipt:
                return True
            else:
                deposit(senderid, amount)
                return False
        else:
            withdraw(receiverid, amount)
            deposit(senderid, amount)
            return False
    else:
        print('Bakiye yetersiz')
        return False


