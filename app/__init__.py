import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.tours.routes import tours_bp
    from app.agencies.routes import agencies_bp
    from app.contact.routes import contact_bp
    from app.admin.routes import admin_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tours_bp, url_prefix='/tours')
    app.register_blueprint(agencies_bp, url_prefix='/agencies')
    app.register_blueprint(contact_bp, url_prefix='/contact')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(errors_bp)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
