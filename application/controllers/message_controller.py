from flask import session
from application import app
from application.database.models import *
from .utils import *
from sqlalchemy import func, or_, and_
from application.database import db
from application.domains.message import PagingMessage


@app.route('/message/my', methods=['GET'])
def get_my_message():
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    res = db.session\
        .query(func.max(Message.sendTime), Message.senderId, Message.receiverId, Message.content, Message.messageId) \
        .group_by(Message.senderId, Message.receiverId) \
        .filter(or_(Message.senderId == user_id, Message.receiverId == user_id))\
        .all()
    result = dict()
    for item in res:
        target_id = item.receiverId if item.senderId == user_id else item.senderId
        if (target_id not in result) or (item[0].timestamp() > result.get(target_id).get("sendTime")):
            result[target_id] = {
                "messageId": item.messageId,
                "senderId": item.senderId,
                "receiverId": item.receiverId,
                "content": item.content,
                "sendTime": item[0].timestamp(),
                "counterpart": User.query.filter(User.userId == target_id).first().to_json_adaptable()
            }
    result = [{"counterpartId": k, **v} for (k, v) in result.items()]
    return make_success_response(result)


@app.route('/message/with/<int:counterpart_id>')
@check_param_from_query_param(PagingMessage)
def get_message_history(param: PagingMessage, counterpart_id: int):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    query = Message.query\
        .filter(or_(and_(Message.senderId == user_id,
                         Message.receiverId == counterpart_id),
                    and_(Message.senderId == counterpart_id,
                         Message.receiverId == user_id)))\
        .order_by(Message.sendTime)
    return make_paging_response(query, param.offset, param.size)
