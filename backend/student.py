from flask import Blueprint, request, jsonify, current_app
from .models import Student, User
from .utils import OTP, role
from . import mail
from flask_mail import Message
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt_identity, get_jwt, jwt_required, current_user, get_csrf_token, unset_access_cookies



bp = Blueprint('student', __name__, subdomain='student')



@bp.post('/signup/')
def signup():
    json = request.json
    try:
        stud: Student = Student.query.filter_by(register_number = json['reg_no']).first()
        if not stud:
            return jsonify(message = 'Student not Found'), 404
        
        if not stud.email:
            return jsonify(message = 'Student Has No email address consult the staff'), 404
        otp = OTP.generate(stud.email)
        if not otp:
            return jsonify(message = "Can't create otp"), 400
        
        msg = Message(
            subject='Email Verification',
            recipients=[stud.email],
            sender=current_app.config['MAIL_USERNAME'],
            body= f"Verification code : {otp}"
        )
        mail.send(msg)

        return jsonify(message = 'OTP was sented'), 200
    except Exception as e:
        print(e)
        return jsonify(message = 'Internel Server Error'), 500



@bp.post('/signup/confirm')
def confirm_signup():
    try:
        token = request.json["otp"]
        reg_no = request.json["reg_no"]
        
        stud: Student = Student.query.filter_by(register_number = reg_no).first()
        email = OTP.verify(token)

        if stud.email != email:
            return jsonify(
                message = "Invalid OTP"
            ), 400

        user = User(role=bp.name, role_id=stud.id, password=None)
        user.save()

        res = jsonify(message = 'Student User Created Successfully!')

        return res

    except Exception as E:
        print(E)
        return jsonify(message = 'Internel Server Error!'), 500





@bp.post('/login/')
def login():
    data: dict = request.json

    if not data or "reg_no" not in data :
        return dict(
            msg = "Unsupported data."
        ), 400
    


    stud: Student = Student.query.filter_by(register_number = data['reg_no']).first()
    if not stud:
        return jsonify(msg = "student not found"), 404
    

    user: User = User.query.filter_by(role = "student", role_id = stud.id).first()
    if not user:
        return jsonify(msg = "user not found!"), 404
    
    if "pwd" in data:
        if User.verify_password(user, data['pwd']) is False:
            return jsonify(msg = "Password Invalid"), 400
        res = jsonify(msg = "login success!")
        token = create_access_token(identity=user)
        set_access_cookies(res, token)
        return res

    try:
        otp = OTP.generate(stud.email)
        msg = Message(
            sender="msec@fastmail.com",
            recipients=[stud.email],
            subject="Email Verification.",

            body=f"code <a>{otp}</a>"
        )
        mail.send(msg)
        return jsonify(
            msg = "otp was sent!"
        )
    except: return jsonify(msg = "can't generate otp"), 500



@bp.post('/login/confirm')
def login_confirm():
    reg_no = request.json['reg_no'] or None
    otp =  request.json['otp'] or None

    if not reg_no or not otp:
        return jsonify(msg = "validation error"), 400
    
    stud = Student.query.filter_by(register_number = reg_no).first()
    if not stud:
        return jsonify(msg = "student not found")
    
    user: User = User.query.filter_by(role = "student", role_id = stud.id).first()

    if not user:
        return jsonify(msg = "Student not registered!"), 404
    
    token = create_access_token(identity=user)
    res = jsonify(msg = "login success!")
    set_access_cookies(res, token)
    return res



@bp.post("/logout/")
@role('student')
def logout():
    res = jsonify(msg = "logout success!")
    unset_access_cookies(res)
    return res




@bp.put('/change_password')
@role('student')
def change_password():
    pwd = request.json["pwd"] or None

    if pwd is None:
        return jsonify("pwd data missind"), 400
    
    user: User = current_user
    user.change_password(pwd)
    user.save()

    return jsonify(msg = "password has changed!")



@bp.get('/class/')
@role('student')
def student_class():
    stud: Student = Student.query.get(current_user.role)
    


@bp.get('/')
@role('student')
def get_student():
    return "hello"