from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class DevConfig(Config):
    DEBUG = True
    DATABASE_URI = getenv('DEV_DATABASE_URI', '')
    SQLALCHEMY_DATABASE_URI = 'postgresql://testdb:test@127.0.0.1:5432/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')
