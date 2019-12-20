from flask import session
from application import app
from .utils import *
from application.database.models import *


@app.route('/user/info/my', methods=['GET'])
def get_my_info():
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    user = User.query.filter(User.userId == user_id).first()
    return make_success_response(user.to_json_adaptable())


@app.route('/user/follow/my', methods=['GET'])
def get_my_follow():
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    user = User.query.filter(User.userId == user_id).first()
    result = {
        "followerNum": user.follower.count(),
        "followeeNum": user.followee.count()
    }
    return make_success_response(result)
