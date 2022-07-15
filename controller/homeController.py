from controller import controllerBlueprint as backend
from flask import render_template, request, flash, redirect, url_for, session, make_response
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
            if request.form.get("event", "") == "updateuser":
                result = userEvents.update(
                    id=request.form.get("id", ""),
                    name=request.form.get("name", ""),
                    surname=request.form.get("surname", ""),
                    email=request.form.get("email", "")
                )
                if result:
                    flash("Kullanıcı başarıyla güncellenmiştir.", "success")
                else:
                    flash("Kullanıcı güncellenirken hata alındı.", "warning")
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
                if userEvents.getamount(request.form.get("id", "")) == 0:
                    result = userEvents.delete(userid=request.form.get("id", ""))
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
            if request.form.get("event", "") == "downloadreceipt":
                return redirect(url_for(".login"))
                result = receiptEvents.view(id=request.form.get("id", "")).pdf
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


@backend.route("/receipt/pdf/<int:id>/")
def receipthtml(id):
    receipt_pdf = receiptEvents.get_receipt_pdf(receipt_id=id)
    if receipt_pdf:
        response = make_response(receipt_pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=receipt.pdf"
        return response
    else:
        return "Not found receipt data."
