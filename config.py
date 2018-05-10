from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI=getenv('postgres://Lukasz:pass:@localhost:5000','')

class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')
