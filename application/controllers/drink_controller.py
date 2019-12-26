from application import app
from application.database.models import *
from application.domains.drink import *
from .utils import *


@app.route('/drink/ofBrand/<int:brand_id>', methods=['GET'])
def get_brand_drinks(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        return make_error_response(WrongCode.ID_NOT_FOUND)
    drinks = [shop.to_json_adaptable() for shop in brand.drinks]
    return make_success_response(drinks)


@app.route('/drink/all', methods=['GET'])
def get_all_drink():
    return make_success_response([drink.to_json_adaptable() for drink in Drink.query().all()])


@app.route('/drink/search', methods=['POST'])
@check_param_from_req_body(DrinkSearchParam)
def search_drink(param: DrinkSearchParam):
    result = Drink.query().filter(Drink.drinkName.like(param.key)).all()
    return make_success_response([drink.to_json_adaptable() for drink in result])
