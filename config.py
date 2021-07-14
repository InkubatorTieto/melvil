from os import getenv


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ""

    # email server
    MAIL_SERVER = getenv("MAIL_SERVER")
    MAIL_PORT = getenv("MAIL_PORT")
    MAIL_USE_TLS = getenv("MAIL_USE_TLS") == "True"
    MAIL_USE_SSL = getenv("MAIL_USE_SSL") == "True"
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    MAIL_SENDER = getenv("MAIL_SENDER")
    MAIL_ADMINS = getenv("MAIL_ADMINS")
    ADMINS = [getenv("MAIL_USERNAME")]

    # database
    DB_ENGINE = getenv("DB_ENGINE")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_DATABASE_URI = "{0}://{1}:{2}@{3}:{4}/{5}".format(
        DB_ENGINE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )

    # LDAP
    LDAP_HOST = getenv("LDAP_HOST")
    LDAP_USERNAME = getenv("LDAP_USERNAME")
    LDAP_PASSWORD = getenv("LDAP_PASSWORD")
    LDAP_BASE_DN = getenv("LDAP_BASE_DN")
    LDAP_LOGIN_VIEW = getenv("LDAP_LOGIN_VIEW")
    LDAP_USER_OBJECT_FILTER = getenv("LDAP_USER_OBJECT_FILTER")

    # admin users
    ADMIN_LIST = getenv("ADMIN_LIST")
    ADMIN_NAME = getenv("ADMIN_NAME")

    # users outside Wroclaw authorized to login
    AUTH_USERS = getenv("AUTH_USERS").split(',')


class DevConfig(Config):
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = "4f\g45t45gfjerkfefker"
    SECURITY_PASSWORD_SALT = "my_precious_two"
    DEBUG = True


class ProdConfig(Config):
    SECRET_KEY = getenv("SECRET_KEY")
    SECURITY_PASSWORD_SALT = getenv("SECURITY_PASSWORD_SALT")
