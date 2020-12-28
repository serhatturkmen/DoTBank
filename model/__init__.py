from flask_sqlalchemy import SQLAlchemy
from dateFunction import getdate

db = SQLAlchemy()


class Card(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True)
    cardnumber = db.Column(db.Text)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    secretkey = db.Column(db.Integer)
    name = db.Column(db.Text)
    userid = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.Text)
    surname = db.Column(db.Text)
    email = db.Column(db.Text)
    amount = db.Column(db.Integer)
    createddate = db.Column(db.Text, default=getdate())


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    senderid = db.Column(db.Integer)
    receiverid = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    detail = db.Column(db.Text)
    processdate = db.Column(db.Text, default=getdate())


class ReceiptPdf(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    receiptid = db.Column(db.Integer)
    pdf = db.Column(db.LargeBinary)
    createddate = db.Column(db.Text, default=getdate())



