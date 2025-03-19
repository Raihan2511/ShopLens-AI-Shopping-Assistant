from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config.config import Config
from app.extensions import db
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config from class

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    CORS(app, resources={r"/api/v1/*": {"origins": "http://localhost:3000"}})
    CORS(app)
    JWTManager(app)

    # Register Blueprints (modular routes)
    # from app.routes import user_bp, chat_bp, message_bp, feedback_bp
    # app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    # app.register_blueprint(chat_bp, url_prefix='/api/v1/chats')
    # app.register_blueprint(message_bp, url_prefix='/api/v1/messages')
    # app.register_blueprint(feedback_bp, url_prefix='/api/v1/feedback')

    return app
