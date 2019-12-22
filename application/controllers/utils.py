from functools import wraps
from flask import request, make_response, jsonify
from enum import Enum
from application.domains.base import DomainBase, RequiredParamNotFoundException


class WrongCode(Enum):
    GENERAL_ERROR = (-200, "Some error occurred.")
    INVALID_ARG = (-201, "Invalid arguments.")
    INVALID_PAGING_OFFSET = (-202, "Paging offset beyond record num.")
    ID_NOT_FOUND = (-203, "Record with given id not found.")
    LOGIN_MISMATCH = (-211, "Mismatch for phone and password.")
    PHONE_EXIST = (-212, "Phone already used.")
    PHONE_NOT_EXIST = (-213, "Phone should exist but not.")
    CODE_SERVICE_ERROR = (-214, "Validate code service unavailable.")
    WRONG_CODE = (-215, "Wrong validate code.")
    NOT_LOGGED = (-216, "Login needed.")


def check_param_from_req_body(param_type: type):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            raw_params = request.json
            if (res := __get_filtered_params(raw_params, param_type)) is not None:
                kwargs['param'] = res
                return f(*args, **kwargs)
            else:
                return make_error_response(WrongCode.INVALID_ARG)
        return decorated
    return wrapper


def check_param_from_query_param(param_type: type):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            query_params = request.args
            if (res := __get_filtered_params(query_params, param_type)) is not None:
                kwargs['param'] = res
                return f(*args, **kwargs)
            else:
                return make_error_response(WrongCode.INVALID_ARG)
        return decorated
    return wrapper


def __get_filtered_params(src, param_type: type):
    if not issubclass(param_type, DomainBase):
        return None
    try:
        res = param_type(**src)
        return res
    except (RequiredParamNotFoundException, TypeError):
        return None


def make_error_response(error: WrongCode):
    payload = {
        "code": error.value[0],
        "message": error.value[1]
    }
    return make_response(jsonify(payload), 200, None)


def make_success_response(data, with_credential=None):
    payload = {
        "code": 200,
        "data": data,
        "withCredential": True if with_credential is not None else None
    }
    return make_response(jsonify(payload), 200, None)


def make_paging_response(sorted_query_object, start, size=None):
    total_num = sorted_query_object.count()
    if start >= total_num:
        return make_error_response(WrongCode.INVALID_PAGING_OFFSET)
    payload = {
        "start": start,
        "size": size,
        "total_num": total_num,
        "next": -1 if start + size >= total_num else start + size,
        "data":
            [item.to_json_adaptable() for item in sorted_query_object.offset(start).limit(size).all()]
            if size is not None else
            [item.to_json_adaptable() for item in sorted_query_object.offset(start).all()]
    }
    return make_success_response(payload)
