from app_instance import app
from controller.apiController import api
from controller.homeController import home

app.register_blueprint(home)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True, port=8580)
