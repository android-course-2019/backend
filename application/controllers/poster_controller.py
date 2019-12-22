from flask import session
from application import app
from .utils import *
from application.database import db
from application.database.models import *
from application.database.relations import *
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
    user = User.query.get(user_id)
    return make_paging_response(user.likedPosters.order_by(Poster.createTime), param.offset, param.size)


@app.route('/poster/my/followed', methods=['GET'])
@check_param_from_query_param(GetPosterParam)
def get_my_followed_posters(param: GetPosterParam):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    if param.offset is None:
        param.offset = 0
    result = Poster.query\
                   .join(UserFollow, Poster.sendById == UserFollow.c.followeeId)\
                   .filter(UserFollow.c.followerId == user_id)\
                   .order_by(Poster.createTime)
    return make_paging_response(result, param.offset, param.size)


@app.route('/poster/create', methods=['POST'])
@check_param_from_req_body(CreatePosterParam)
def create_poster(param: CreatePosterParam):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    poster = Poster(content=param.content, sendById=user_id)
    db.session.add(poster)
    db.session.commit()

    poster_id = poster.posterId

    for drink in param.drinks:
        if isinstance(drink, str):
            poster_drink = PosterDrink(posterId=poster_id, drinkName=param.brandName+' '+drink)
        else:
            poster_drink = PosterDrink(posterId=poster_id, drinkId=drink)
        db.session.add(poster_drink)

    # TODO("finish file api")

