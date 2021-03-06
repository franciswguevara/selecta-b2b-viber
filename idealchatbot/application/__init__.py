from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()

def create_app():
    '''Construct the core app object'''
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .code import *
        #from .assets import compile_assets
        
        # Create Viberbot
        viber = New_Api(New_BotConfiguration(
            name='Selecta B2B',
            avatar='https://i.imgur.com/YxAFDbx.png',
            auth_token = access_token
        ))

        # Register Blueprints
        # app.register_blueprint(routes.main_bp)
        # app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()
        
        return app


