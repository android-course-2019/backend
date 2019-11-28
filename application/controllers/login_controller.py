from flask import session
from application import app
from application.domains.login import *
from .utils import *
from application.database import db
from application.database.models import *
from application.services.validate_code import send_validate_code, check_validate_code, ValidateCodeError


class LoginWrongCode(BaseWrongCode):
    GENERAL_ERROR = (-200, "Some error occurred.")
    LOGIN_MISMATCH = (-201, "Mismatch for phone and password")
    PHONE_EXIST = (-202, "Phone already used.")
    CODE_SERVICE_ERROR = (-203, "Validate code service unavailable.")
    WRONG_CODE = (-204, "Wrong validate code.")


@app.route('/login', methods=['POST'])
@check_param(LoginParam)
def login(param: LoginParam):
    tmp_user = User(phone=param.phone, password=param.password)
    res = User.query.filter(User.phone == tmp_user.phone).all()
    if len(res) != 1:
        return make_error_response(LoginWrongCode.LOGIN_MISMATCH)
    if tmp_user.password != res[0].password:
        return make_error_response(LoginWrongCode.LOGIN_MISMATCH)
    session['userId'] = res[0].userId
    return make_success_response("ok")


@app.route('/signUp', methods=['POST'])
@check_param(SignUpParam)
def sign_up(param: SignUpParam):
    if User.query.filter(User.phone == param.phone).count() != 0:
        return make_error_response(LoginWrongCode.PHONE_EXIST)

    res = check_validate_code(param.phone, param.validateCode)
    if isinstance(res, ValidateCodeError):
        if res == ValidateCodeError.ARGUMENT_INVALID:
            return make_error_response(LoginWrongCode.GENERAL_ERROR)
        elif res == ValidateCodeError.SERVICE_UNAVAILABLE:
            return make_error_response(LoginWrongCode.CODE_SERVICE_ERROR)
        elif res == ValidateCodeError.CODE_NOT_SENT or res == ValidateCodeError.WRONG_CODE:
            return make_error_response(LoginWrongCode.WRONG_CODE)
    else:
        new_user = User(phone=param.phone, password=param.password)
        db.session.add(new_user)
        db.session.commit()
        return make_success_response('ok')


@app.route('/sendSms', methods=['POST'])
@check_param(SendSmsParam)
def send_sms(param: SendSmsParam):
    if param.checkExist:
        if User.query.filter(User.phone == param.phone).count() != 0:
            return make_error_response(LoginWrongCode.PHONE_EXIST)

    res = send_validate_code(param.phone)
    if isinstance(res, ValidateCodeError):
        if res == ValidateCodeError.SERVICE_UNAVAILABLE:
            return make_error_response(LoginWrongCode.CODE_SERVICE_ERROR)
        else:
            return make_error_response(LoginWrongCode.GENERAL_ERROR)
    else:
        return make_success_response('ok')
