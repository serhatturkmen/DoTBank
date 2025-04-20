from flask import Flask
from model import db
from dotenv import load_dotenv
import os
from controller.apiController import api
from controller.homeController import home

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("MY_SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
