from flask import session
from application import app
from .utils import *
from sqlalchemy import and_
from application.database import db
from application.database.models import *
from application.database.relations import *


@app.route('/user/my/info', methods=['GET'])
def get_my_info():
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    user = User.query.filter(User.userId == user_id).first()
    return make_success_response(user.to_json_adaptable())


@app.route('/user/info/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
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


@app.route('/user/follow/<int:other_user_id>', methods=['POST'])
def follow(other_user_id):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    UserFollow.insert().values(followerId=user_id, followeeId=other_user_id)
    db.session.commit()
    return make_success_response('ok')


@app.route('/user/unfollow/<int:other_user_id>', methods=['POST'])
def unfollow(other_user_id):
    # FIXME
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    db.session.query(UserFollow).filter(
       and_(UserFollow.c.followerId == user_id,
            UserFollow.c.followeeId == other_user_id)
    ).delete()
    db.session.commit()
    return make_success_response('ok')
