from flask import session
from application import app
from application.domains.login import *
from .utils import *
from application.database.models import *


class LoginWrongCode(BaseErrorCode):
    LOGIN_MISMATCH = (-201, "Mismatch for phone and password")
    PHONE_EXIST = (-202, "Phone already used.")


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

