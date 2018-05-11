from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        getenv('DEV_DATABASE_URI',
               'postgresql://super_user:qwerty1234@127.0.0.1:5432/psql_db'))


class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')
