from flask import session
from application import app
from application.domains.auth import *
from .utils import *
from application.database import db
from application.database.models import *
from application.services.validate_code import send_validate_code, check_validate_code, ValidateCodeError


@app.route('/auth/login', methods=['POST'])
@check_param_from_req_body(LoginParam)
def login(param: LoginParam):
    tmp_user = User(phone=param.phone, password=param.password)
    res = User.query.filter(User.phone == tmp_user.phone).first()
    if res is None:
        return make_error_response(WrongCode.LOGIN_MISMATCH)
    if tmp_user.password != res.password:
        return make_error_response(WrongCode.LOGIN_MISMATCH)
    session['userId'] = res.userId
    return make_success_response("ok", with_credential=True)


@app.route('/auth/signUp', methods=['POST'])
@check_param_from_req_body(SignUpParam)
def sign_up(param: SignUpParam):
    if User.query.filter(User.phone == param.phone).count() != 0:
        return make_error_response(WrongCode.PHONE_EXIST)

    res = check_validate_code(param.phone, param.validateCode)
    if isinstance(res, ValidateCodeError):
        if res == ValidateCodeError.ARGUMENT_INVALID:
            return make_error_response(WrongCode.GENERAL_ERROR)
        elif res == ValidateCodeError.SERVICE_UNAVAILABLE:
            return make_error_response(WrongCode.CODE_SERVICE_ERROR)
        elif res == ValidateCodeError.CODE_NOT_SENT or res == ValidateCodeError.WRONG_CODE:
            return make_error_response(WrongCode.WRONG_CODE)
    else:
        new_user = User(phone=param.phone, password=param.password, nickName=param.nickName)
        db.session.add(new_user)
        db.session.commit()
        session['userId'] = new_user.userId
        return make_success_response('ok', with_credential=True)


@app.route('/auth/sendSms', methods=['POST'])
@check_param_from_req_body(SendSmsParam)
def send_sms(param: SendSmsParam):
    if param.checkExist is not None:
        exist = User.query.filter(User.phone == param.phone).count() != 0
        if exist and not param.checkExist:
            return make_error_response(WrongCode.PHONE_EXIST)
        if param.checkExist and not exist:
            return make_error_response(WrongCode.PHONE_NOT_EXIST)

    res = send_validate_code(param.phone)
    if isinstance(res, ValidateCodeError):
        if res == ValidateCodeError.SERVICE_UNAVAILABLE:
            return make_error_response(WrongCode.CODE_SERVICE_ERROR)
        else:
            return make_error_response(WrongCode.GENERAL_ERROR)
    else:
        return make_success_response('ok')


@app.route('/auth/logout', methods=['POST'])
def logout():
    if session.get('userId') is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    session.pop('userId')
    return make_success_response('ok')
