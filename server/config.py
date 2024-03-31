# Path: server/config.py

from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_ECHO = False
    TESTING = True
