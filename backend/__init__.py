from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from flask import Flask
from .models import *

jwt = JWTManager()
mg = Migrate()
crypt = Bcrypt()
mail = Mail()

import backend.utils

def create_app(conifg: object) -> Flask :
    app = Flask(__name__)
    from flask_jwt_extended import current_user, jwt_required

    # Configuration 
    app.config.from_object(conifg)
    db.init_app(app)
    jwt.init_app(app)
    mg.init_app(app, db)
    crypt.init_app(app)
    mail.init_app(app)

    from backend.hod import hod
    app.register_blueprint(hod)

    from backend.student import bp as student
    app.register_blueprint(student)
    
    from werkzeug.exceptions import HTTPException
    from flask import jsonify
    @app.errorhandler(HTTPException)
    def error_handler(e):
        res = jsonify(
            error = e.description
        )
        return res, e.code

    with app.app_context():
        db.create_all()

    return app

