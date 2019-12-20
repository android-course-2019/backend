from flask import session
from application import app
from .utils import *
from application.database.models import *
from application.domains.poster import *


@app.route('/poster/my/created', methods=['GET'])
@check_param_from_query_param(GetPosterParam)
def get_my_created_posters(param: GetPosterParam):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    if param.offset is None:
        param.offset = 0
    return make_paging_response(Poster.query.filter(Poster.sendById == user_id), param.offset, param.size)


@app.route('/poster/my/liked', methods=['GET'])
@check_param_from_query_param(GetPosterParam)
def get_my_liked_posters(param: GetPosterParam):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    if param.offset is None:
        param.offset = 0
    user = User.query.filter(User.userId == user_id).first()
    return make_paging_response(user.likedPosters.order_by(Poster.createTime), param.offset, param.size)
