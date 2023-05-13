from flask import Flask
from model import db
from controller import controllerBlueprint
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

print(os.getenv("EMAIL_PASSWORD"))

app.config['SECRET_KEY'] = os.getenv("MY_SECRET")
app.register_blueprint(controllerBlueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veritabani.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=8580)
