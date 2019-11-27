from application.database.models import User
from application.services.sms import send_sms
from application.services.redis import redis


def send_validate_code(phone, check_exist=False):
    if not isinstance(phone, str) or len(phone) != 11:
        return False, "Argument 'phone' invalid. Got: {}".format(phone)

    if check_exist:
        result = User.query.filter_by(phone=phone).all()
        if len(result) != 0:
            return False, "Phone num already exists!"

    success, result = send_sms(phone)
    if success:
        redis.set("{}_validate".format(phone), str(result), ex=300)
    else:
        return False, "Sms service Error. Detail: {}".format(result)


def check_validate_code(phone, valid_code):
    if not isinstance(phone, str) or len(phone) != 11:
        return False, "Argument 'phone' invalid. Got: {}".format(phone)

    if not isinstance(valid_code, str) or len(valid_code) != 6:
        return False, "Argument 'phone' invalid. Got: {}".format(valid_code)

    key = "{}_validate".format(phone)

    if key not in redis:
        return False, "Validate code not set."

    if redis.get(key) != valid_code:
        return False, "Wrong validate code."

    return True
