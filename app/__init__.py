from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .cart_items import bp as cart_bp
    app.register_blueprint(cart_bp)

    from .cart_form import bp as cart_form_bp
    app.register_blueprint(cart_form_bp)

    from .getPurchases import bp as purchases_bp
    app.register_blueprint(purchases_bp)

    from .purchases_form import bp as purchases_form_bp
    app.register_blueprint(purchases_form_bp)

    return app
