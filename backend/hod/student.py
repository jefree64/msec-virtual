from flask import Blueprint, request, jsonify, abort
from ..models import Student, Hod, Department, IntegrityError
from ..utils import role, validate_json
from flask_jwt_extended import current_user
from http import HTTPStatus

bp = Blueprint('student', __name__, url_prefix='/students')


@bp.get('/')
@role('hod')
def students():
    data = Student.query.filter_by(dept_id = current_user.dept_id).all()
    return jsonify(students = data)

@bp.post('/')
@role('hod')
@validate_json('reg_no', 'name', 'email', optional=['mobile_no'])
def add_student():
    reg_no = request.json['reg_no']
    name = request.json['name']
    email = request.json['email']
    mobile_no = request.json['mobile_no'] or None

    try:
        dpt = Department.query.get(current_user.dept_id)
        stud = Student(register_number=reg_no, name=name, dept_id=dpt.id, dept_name=dpt.name, email=email, mobile_number=mobile_no)
        stud.save()
    except IntegrityError: abort(HTTPStatus.FORBIDDEN,'student register number already exist')
    
    return jsonify(msg = 'student added success', student = stud)


