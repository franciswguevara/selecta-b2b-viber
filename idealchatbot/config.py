from dotenv import load_dotenv
import os
import redis


load_dotenv()
Class Config:
    """Set Flask configuration from environment variables"""
    
    # General Config
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Viberbot
    access_token = os.getenv("CHATBOT_TOKEN")

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    SESSION_REDIS = redis.from_url(os.getenv('REDIS_TLS_URL'))
