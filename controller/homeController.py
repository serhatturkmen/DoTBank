from controller import controllerBlueprint as backend
from flask import render_template, request, flash, redirect, url_for, session
from model import userEvents, cardEvents, receiptEvents
from flask_weasyprint import render_pdf, HTML


@backend.route("/", methods=["GET", "POST"])
def home():
    if session.get("login", ""):
        return render_template("index.html")
    else:
        return redirect(url_for(".login"))


@backend.route("/user/", methods=["GET", "POST"])
def user():
    if session.get("login", ""):
        #todo hesap silinirken kartı olup olmadığına bak
        if request.method == "POST":
            if request.form.get("event", "") == "adduser":
                result = userEvents.add(
                    name=request.form.get("name", ""),
                    surname=request.form.get("surname", ""),
                    amount=request.form.get("amount", ""),
                    email=request.form.get("email", "")
                )
                if result:
                    flash("Kullanıcı başarıyla eklenmiştir.", "success")
                else:
                    flash("Kullanıcı eklenirken hata alındı.", "warning")
            if request.form.get("event", "") == "submitdeposit":
                result = userEvents.deposit(
                    userid=request.form.get("userid", ""),
                    quantity=int(request.form.get('depositmoney', '').replace(",", "").replace(".", ""))
                )
                if result:
                    flash("Para başarıyla yatırılmıştır.", "success")
                else:
                    flash("Para yatırma işlemi başarısız sonuçlandı.", "warning")
            if request.form.get("event", "") == "withdraw":
                result = userEvents.withdraw(
                    userid=request.form.get("userid", ""),
                    quantity=int(request.form.get('withdrawmoney', '').replace(",", "").replace(".", ""))
                )
                if result:
                    flash("Para başarıyla çekilmiştir.", "success")
                else:
                    flash("Para çekme işlemi başarısız sonuçlandı.", "warning")
            if request.form.get("event", "") == "deleteuser":
                if userEvents.getamount(request.form.get("accountid", "")) == 0:
                    result = userEvents.delete(userid=request.form.get("accountid", ""))
                    if result:
                        flash("Kullanıcı başarıyla silinmiştir.", "success")
                else:
                    flash("Kullanıcı silinmesi için bakiyenin sıfır olması gerekmektedir.", "warning")
            return redirect(request.url)
        users = userEvents.viewall()
        return render_template("user.html", users=users, amountformat=userEvents.amountformatter)
    else:
        return redirect(url_for(".login"))


@backend.route("/card/", methods=["GET", "POST"])
def card():
    if session.get("login", ""):
        if request.method == "POST":
            if request.form.get("event", "") == "addcart":
                result = cardEvents.add(
                    cardnumber=request.form.get("cardnumber", ""),
                    year=request.form.get("year", ""),
                    month=request.form.get("month", ""),
                    secretkey=request.form.get("secretkey", ""),
                    name=request.form.get("name", ""),
                    userid=request.form.get("userid", "")
                )
                if result:
                    flash("Kullanıcı başarıyla eklenmiştir.", "success")
            if request.form.get("event", "") == "deletecard":
                result = cardEvents.delete(id=request.form.get("id", ""))
                if result:
                    flash("Kart başarıyla silinmiştir.", "success")
                else:
                    flash("Kart silme başarısız oldu.", "warning")
        return render_template("card.html", cards=cardEvents.viewall(), users=userEvents.viewall())
    else:
        return redirect(url_for(".login"))


@backend.route("/receipt/", methods=["GET", "POST"])
def receipt():
    if session.get("login", ""):
        if request.method == "POST":
            if request.form.get("event", "") == "deletereceipt":
                result = receiptEvents.delete(id=request.form.get("id", ""))
                if result:
                    flash("Dekont başarıyla silinmiştir.", "success")
                else:
                    flash("Dekont silme başarısız oldu.", "warning")
        return render_template("receipt.html", receipts=receiptEvents.viewall(), user=userEvents.view, amountformat=userEvents.amountformatter)
    else:
        return redirect(url_for(".login"))


@backend.route('/logout/', methods=["GET", "POST"])
def logout():
    session['login'] = False
    return redirect(url_for(".login"))
    
@backend.route('/login/', methods=["GET", "POST"])
def login():
    if session.get('login', ''):
        return redirect(url_for('.home'))
    else:
        if request.method == "POST":
            result = userEvents.login(
                username=request.form.get("username", ""),
                password=request.form.get("pass", "")
            )
            if result:
                return redirect(url_for(".home"))
        return render_template("login.html")


# test
@backend.route("/receipt/show/<int:id>/")
def showreceiptpdf(id):
    return render_pdf(url_for('.receipthtml', id=id))


@backend.route("/receipt/download/<int:id>/")
def downloadreceiptpdf(id):
    return render_pdf(url_for('.receipthtml', id=id))


@backend.route('/hello')
def hello_pdf():
    # Make a PDF from another view
    pdfdata = render_pdf(url_for(".receipthtml")).data

    # save file data
    pdffile = open("receipt.pdf", 'wb')
    pdffile.write(pdfdata)
    pdffile.close()

    # save database
    receiptEvents.add(senderid=1, receiverid=2, amount=1000, detail="sıcakyemek.online adresinde 0,10 TL harcama yapıldı.")

    return render_pdf(url_for('.test'))


@backend.route('/hello.pdf')
def hellopdf():
    data = {
        "cardnumber": "1111********4444",
        "processdate": "29 Kasım 2020 01:45:20",
        "processdetail": "detail",
        "amount": "0,10"
    }
    html = render_template("receiptpdftemplate.html", data=data)
    # Make a PDF straight from HTML in a string.
    return render_pdf(HTML(string=html))

