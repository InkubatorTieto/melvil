from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class DevConfig(Config):
    SECRET_KEY = '4f\g45t45gfjerkfefker'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    DB_ENGINE = getenv('DB_ENGINE')
    DB_USER = getenv('DB_USER')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_HOST = getenv('DB_HOST')
    DB_PORT = getenv('DB_PORT')
    DB_NAME = getenv('DB_NAME')
    SECRET_KEY = getenv('SECRET_KEY') or 'blaah'

    SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
        DB_ENGINE,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )

    # email server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    ADMINS = [getenv('MAIL_USERNAME')]


class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')
