from flask import Blueprint, request, jsonify, abort
from ..utils import role, validate_json
from ..models import Class, User, Department, Student, IntegrityError
from flask_jwt_extended import current_user
from http import HTTPStatus

bp = Blueprint('class', __name__)
user: User = current_user


@bp.get('/')
@role('hod')
def get_classes():

    classes: list = Class.query.filter_by(dept_id = user.dept_id).all()
    if not classes:
        abort(404, description = "it Department have no classes")

    return jsonify(classes = classes)


@bp.get("/<int:year>")
@role('hod')
def get_class(year: int):
    _class: Class = Class.query.filter_by(dept_id = user.dept_id).filter_by(year = year).first_or_404()

    return jsonify(_class)


@bp.get('/<int:year>/students/')
@role('hod')
def students(year: int):
    cls: Class = Class.query.filter_by(dept_id = user.dept_id).filter_by(year = year).first()

    return jsonify(students = cls.students)


@bp.post('/<int:year>/students/')
@role('hod')
@validate_json('reg_no', 'name', 'email', optional=['mobile_no'])
def add_students(year: int):
    cls: Class = Department.get_class(user.dept_id, year)
    
    if not cls:
        abort(400)
    
    ...
    try:
        name = request.json['name']
        reg_no = request.json['reg_no']
        email = request.json['email']
        mobile_no = request.json['mobile_no'] or None
        

        stud: Student = Student(reg_no, name, user.id, Department.get_name(user.dept_id), email, mobile_no)
        stud.save()
    
        cls.add_student(stud)
    except IntegrityError: return jsonify(msg = "student has exist with this registered number"), HTTPStatus.FORBIDDEN
    ...

    return jsonify(msg = "Student was added!"), HTTPStatus.CREATED


@bp.post('/<int:year>/students/upload')
@role('hod')
def upload_student(year: int):
    ...

