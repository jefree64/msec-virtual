from flask import Blueprint
from .auth import auth
from .student import bp as student
from ._class import bp as _class

hod = Blueprint('hod', __name__, subdomain='hod')

hod.register_blueprint(auth)
hod.register_blueprint(student)
hod.register_blueprint(_class, url_prefix = '/class')



