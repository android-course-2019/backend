from functools import wraps
import json
from flask import request, make_response
from enum import Enum
from application.domains.base import DomainBase, RequiredParamNotFoundException


class BaseErrorCode(Enum):
    pass


def check_param(param_type: type):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            raw_params = request.json

            if (res := __get_filtered_params(raw_params, param_type)) is not None:
                kwargs['param'] = res
                return f(*args, **kwargs)
            else:
                return 'fail', 400, None
        return decorated
    return wrapper


def __get_filtered_params(src, param_type: type):
    if not issubclass(param_type, DomainBase):
        return None
    try:
        res = param_type(src)
        return res
    except RequiredParamNotFoundException:
        return None


def make_error_response(error: BaseErrorCode):
    payload = {
        "code": error.value[0],
        "message": error.value[1]
    }
    return make_response(json.dumps(payload), 200, None)


def make_success_response(data):
    payload = {
        "code": 200,
        "data": data
    }
    return make_response(json.dumps(payload), 200, None)
