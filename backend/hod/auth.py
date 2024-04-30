from flask import Blueprint, request, jsonify, abort
from ..utils import role, OTP, send_otp, validate_json
from ..models import User, Hod
from flask_jwt_extended import create_access_token, set_access_cookies, current_user, unset_jwt_cookies, jwt_required, get_jwt_identity, create_refresh_token, set_refresh_cookies


auth = Blueprint('hod_auth', __name__)


"""

202 Accepted => OTP validation Successful

403 Forbidden => which will return once all of the allowed attempts are reached to verify the code and were all unsuccessful (three by default) or the OTP code has expired (after five minutes, by default)

410 Gone => Once an OTP reaches a final state (verified, expired or failed after too many attempts), the API always returns HTTP response code "410 Gone"

401 => OTP is not valid ( Unauthorized ).

"""



@auth.post('/login/')
@validate_json('email', optional=['password'])
def login():
    email = request.json['email']
    
    hod: Hod = Hod.query.filter_by(email = email).first()
    if hod is None:
        abort(404, "invalid Email")
    
    user: User = User.get('hod', hod.id)

    if user is None:
        return abort(404,"Hod account not activated!")
    
    try: otp = OTP.generate(email)
    except: abort(500, description = "can't generate otp!")

    send_otp(email, otp)

    return jsonify(msg = "otp was sent!")



@auth.post('/login/confirm')
@validate_json('email', 'otp')
def confirm_login():
    email = request.json['email']
    otp = request.json['otp']
    
    if email != OTP.verify(otp):
        abort(401,"otp is invalid")
    
    hod: Hod = Hod.query.filter_by(email = email).first()
    user: User = User.get('hod', hod.id)

    token = create_access_token(identity=user)
    ref_token = create_refresh_token(identity=user)

    res = jsonify(msg = "login success!")
    set_access_cookies(res, token)
    set_refresh_cookies(res, ref_token)
    return res, 202



@auth.post('/logout')
@jwt_required()
def logout():
    res = jsonify(msg = "logout")

    unset_jwt_cookies(res)
    return res



@auth.post('/refresh')
@role('hod', refresh=True)
def refresh_access_token():
    id = get_jwt_identity()
    token = create_access_token(identity=id, fresh=False)
    res = jsonify(token = token)
    set_access_cookies(res, token)
    return res


