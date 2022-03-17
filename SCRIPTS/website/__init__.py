from flask import Flask
from config import Config
from flask_excel import init_excel
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.debug = True
    init_excel(app)
    app.config.from_object(Config)
    Session(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app