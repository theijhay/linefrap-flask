import os
from dotenv import load_dotenv

""" Load environment variables from .env file """
load_dotenv()

class BaseConfig:
    """ Base configuration class """
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

class DevelopmentConfig(BaseConfig):
    """ Development configuration class """
    DEBUG = True

class ProductionConfig(BaseConfig):
    """ Production configuration class """
    DEBUG = False
