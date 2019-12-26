from flask import session
from application import app
from .utils import *
from sqlalchemy import and_
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


@app.route('/poster/hot', methods=['GET'])
@check_param_from_query_param(GetPosterParam)
def get_hot_posters(param: GetPosterParam):
    if param.offset is None:
        param.offset = 0
    result = Poster.query
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


@app.route('/poster/info/<int:poster_id>', methods=['GET'])
def get_poster_info(poster_id: int):
    poster = Poster.query.get(poster_id)
    if poster is None:
        return make_error_response(WrongCode.ID_NOT_FOUND)
    poster_obj = poster
    poster = poster.to_json_adaptable()
    if (user_id := session.get('userId')) is not None:
        poster['liked'] = \
            User.query.get(user_id).likedPosters.filter(Poster.posterId == poster_obj.posterId).count() != 0
        poster['followed'] = \
            db.session.query(UserFollow).filter(
                and_(UserFollow.c.followerId == user_id,
                     UserFollow.c.followeeId == poster_obj.sendById
                     )).count() != 0
    return make_success_response(poster)


@app.route('/poster/like/<int:poster_id>', methods=['POST'])
def like_poster(poster_id):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    User.query.get(user_id).likedPosters.append(Poster.query.get(poster_id))
    db.session.commit()
    return make_success_response('ok')


@app.route('/poster/unlike/<int:poster_id>', methods=['POST'])
def unlike_poster(poster_id):
    if (user_id := session.get('userId')) is None:
        return make_error_response(WrongCode.NOT_LOGGED)
    User.query.get(user_id).likedPosters.remove(Poster.query.get(poster_id))
    db.session.commit()
    return make_success_response('ok')
