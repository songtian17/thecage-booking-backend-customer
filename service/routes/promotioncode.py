from flask import jsonify
from service import app
from service import PromoCode, promo_code_schema, promo_codes_schema

# Get PromotionCodes
@app.route("/promotioncodes", methods=['GET'])
def get_promo_code():
    promocode = PromoCode.query.all()
    result = promo_codes_schema.dump(promocode)
    return jsonify(result)

# Get PromotionCode based on Id
@app.route("/promotioncode/<Id>", methods=['GET'])
def get_promo_code_based_on_id(Id):
    promocode = PromoCode.query.get(Id)
    return promo_code_schema.jsonify(promocode)