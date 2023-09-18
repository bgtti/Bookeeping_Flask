from flask import Flask
from app.config import Config
import app.extensions as extensions
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    extensions.db.init_app(app)
    extensions.flask_bcrypt.init_app(app)
    # extensions.auth.init_app(app)  
    extensions.jwt.init_app(app)
    extensions.cors.init_app(app)
    # login_manager = LoginManager()

    from app.models import user_workspace
    # from app.error_handlers.routes import error_handler
    from flask import current_app

    from app.account.routes import account
    from app.expenses.routes import expenses
    from app.workspace_settings.routes import workspace_settings
    app.register_blueprint(account, url_prefix='/api/account')
    app.register_blueprint(workspace_settings, url_prefix='/api/workspace_settings')
    app.register_blueprint(expenses)

    @app.route('/test/')
    def test_page():
        return '<h1> Testing the App </h1>'

    # ABS_PATH = os.path.dirname(__file__)
    # REL_PATH = "static"
    # STATIC_PATH = repr(str(app.config["STATIC_FOLDER"]))

    # @app.route("/../static/<filename>")
    # def static_path():
    #     pass

    return app
