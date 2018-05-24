from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    DB_ENGINE = getenv('DB_ENGINE')
    DB_USER = getenv('DB_USER')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_HOST = getenv('DB_HOST')
    DB_PORT = getenv('DB_PORT')
    DB_NAME = getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
        DB_ENGINE,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )


class ProdConfig(Config):
    DATABASE_URI = getenv('PROD_DATABASE_URI', '')


class TestConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True
    DB_ENGINE = getenv('TEST_DB_ENGINE')
    DB_USER = getenv('TEST_DB_USER')
    DB_PASSWORD = getenv('TEST_DB_PASSWORD')
    DB_HOST = getenv('TEST_DB_HOST')
    DB_PORT = getenv('TEST_DB_PORT')
    DB_NAME = getenv('TEST_DB_NAME')

    SQLALCHEMY_DATABASE_URI = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
        DB_ENGINE,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )
