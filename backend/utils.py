from itsdangerous import URLSafeTimedSerializer
from flask import current_app, request
from backend import jwt
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt, verify_jwt_in_request
from functools import wraps
from flask_mail import Message
from . import mail
from http import HTTPStatus



class OTP:
        @classmethod
        def secret_key(cls):
             with current_app.app_context():
                  return current_app.config['SECRET_KEY']
        
        @classmethod
        def password_salt(cls):
             with current_app.app_context():
                  return current_app.config['SECURITY_PASSWORD_SALT']

        @classmethod
        def generate(cls, email: str) -> str:
            sr = URLSafeTimedSerializer(secret_key=cls.secret_key(), salt=cls.password_salt())
            return sr.dumps(email)
        
        @classmethod
        def verify(cls, token: str, exp = 3600) -> str:
            sr = URLSafeTimedSerializer(secret_key=cls.secret_key(), salt=cls.password_salt())
            try:
                email = sr.loads(token, exp)
                return email
            except:
                return False








@jwt.user_identity_loader
def user_id_loader(user):
    return user.id

@jwt.user_lookup_loader
def user_loader(header, data):
    id = data['sub']

    from backend.models import User
    return User.query.get(id)



def role(*role, fresh: bool = False, refresh: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*ar,**arr):
            verify_jwt_in_request(fresh=fresh, refresh=refresh)
            from flask_jwt_extended import current_user
            usr = current_user  
            if usr.role not in role:
                return dict(message = 'Permission Denied!'), HTTPStatus.UNAUTHORIZED
            
            return func(*ar, **arr)
        return wrapper
    return decorator




def send_otp(email: str, otp: str):
    msg = Message(
        subject='Email Verification',
        recipients=[email],
        sender='msec@fastmail.com',
        body=f"verification code: {otp}"
    )

    mail.send(msg)




def validate_json(*fields, optional: list[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return dict(msg = "Server should only accept (content-type: 'application/json')"), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            if len(fields) != 0 :
                data: dict = dict(request.json)
                if optional:
                    for i in optional:
                        data.pop(i, 0)
                if list(fields) != list(data):
                    return dict(msg = f"Must Have {set(fields)} fields"), HTTPStatus.UNPROCESSABLE_ENTITY
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
            
def validate_file(*fields):
    ...


