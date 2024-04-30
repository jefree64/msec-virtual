from random import randbytes
from datetime import timedelta


class Config(object):
    SECRET_KEY = str(randbytes(54))
    SQLALCHEMY_DATABASE_URI = "sqlite:///db"
    
    # JWT
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_CSRF_IN_COOKIES = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


    # OTP serializer
    SECURITY_PASSWORD_SALT = str(randbytes(6))
    
    # Mail Settings
    MAIL_SERVER = "smtp.fastmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = 'msec@fastmail.com'
    MAIL_PASSWORD = 'adggvnylruxb2npa'

    # Server settings
    SERVER_NAME = 'msec.edu:5000'
    ...

class DevConfig(Config):
    ...