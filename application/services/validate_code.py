from enum import Enum
from application.services.sms import send_sms
from application.services.redis import redis


class ValidateCodeError(Enum):
    ARGUMENT_INVALID = -1
    SERVICE_UNAVAILABLE = -2
    CODE_NOT_SENT = -3
    WRONG_CODE = -4


def send_validate_code(phone):
    if not isinstance(phone, str) or len(phone) != 11:
        return ValidateCodeError.ARGUMENT_INVALID

    success, result = send_sms(phone)
    if success:
        redis.set("{}_validate".format(phone), str(result), ex=300)
    else:
        return ValidateCodeError.SERVICE_UNAVAILABLE
    return True


def check_validate_code(phone, valid_code):
    if not isinstance(phone, str) or len(phone) != 11:
        return ValidateCodeError.ARGUMENT_INVALID

    if not isinstance(valid_code, str) or len(valid_code) != 6:
        return ValidateCodeError.ARGUMENT_INVALID

    key = "{}_validate".format(phone)

    if key not in redis:
        return ValidateCodeError.CODE_NOT_SENT

    if str(redis.get(key), encoding='utf-8') != valid_code:
        return ValidateCodeError.WRONG_CODE

    return True
