from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://Lukasz:pass:@localhost:5000'


class DevConfig(Config):
    DEBUG = True
    DATABASE_URI = getenv('DEV_DATABASE_URI', '')


class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')
