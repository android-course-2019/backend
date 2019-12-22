from application import app
from application.database.models import *
from .utils import *


@app.route('/shop/ofBrand/<int:brand_id>', methods=['GET'])
def get_brand_shops(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        return make_error_response(WrongCode.ID_NOT_FOUND)
    shops = [shop.to_json_adaptable() for shop in brand.shops.all()]
    return make_success_response(shops)
