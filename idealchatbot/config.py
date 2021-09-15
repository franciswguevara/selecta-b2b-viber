from dotenv import load_dotenv
import os

load_dotenv()
Class Config:
    """Set Flask configuration from environment variables"""
    
    access_token = os.getenv("CHATBOT_TOKEN")

    # Flask-SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS = False