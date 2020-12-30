from controller import controllerBlueprint as api
from flask import request, jsonify
from model import cardEvents, userEvents


# curl -X POST -F 'cardnumber=1111222233334444' -F 'year=2023' -F 'month=10' -F 'name=JOHN DOE' -F 'secretkey=145' http://127.0.0.1:8580/api/v1.0/trust/
@api.route("/api/v1.0/trust/", methods=["POST"])
def apitrust():
    result = cardEvents.trust(
        cardnumber=request.form.get("cardnumber", ""),
        secretkey=request.form.get("secretkey", ""),
        year=request.form.get("year", ""),
        month=request.form.get("month", ""),
        name=request.form.get("name", "")
    )
    if not result:
        return jsonify({
            "error": "true",
            "id": "none"
        })
    else:
        return jsonify({
            "error": "false",
            "id": result
        })


# curl -X POST -F 'receiverid=1' -F 'senderid=2' -F 'amount=10' http://127.0.0.1:8580/api/v1.0/getpay/
@api.route("/api/v1.0/getpay/", methods=["POST"])
def apigetpay():
    senderid = int(request.form.get("senderid", ""))
    receiverid = int(request.form.get("receiverid", ""))
    amount = int(request.form["amount"])
    if amount <= userEvents.view(senderid).amount:
        result = userEvents.sendmoney(
            senderid=senderid,
            receiverid=receiverid,
            amount=amount
        )
        if result:
            return jsonify({"result": "Ödeme başarılı", "statu": True})
        else:
            return jsonify({"result": "Ödeme başarısız", "statu": False})
    else:
        return jsonify({"result": "Yetersiz bakiye", "statu": False})

