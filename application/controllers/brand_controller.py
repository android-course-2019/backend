from application import app
from application.database.models import *
from .utils import *


@app.route('/brand/all', methods=['GET'])
def get_all_brand():
    result = Brand.query.all()
    return make_success_response([x.to_json_adaptable() for x in result])
