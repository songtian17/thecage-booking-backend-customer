from flask import request, jsonify
from service import app
from service.models import PromoCode, PromoCodeLog, promo_code_schema, promo_codes_schema, CartItem, cart_items_schema
import jwt
from datetime import datetime
from service import db
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


# Enter PromoCode
@app.route("/promotioncode", methods=["POST"])
def enter_promo_code():
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    customer_id = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]

    code_name = request.json["promoCode"]
    promocode = PromoCode.query.all()
    result = promo_codes_schema.dump(promocode)
    # print(result)
    code_does_not_exist = False
    for i in result:
        if i["code"] == code_name:
            code_id = i["id"]

            apply_promocode = PromoCode.query.get(code_id)
            print(apply_promocode)
            if apply_promocode.valid_to < datetime.now():
                return "Promo Code applied has expired", 400
            
            if apply_promocode.valid_from > datetime.now():
                return "Promo Code applied is invalid", 400

            if apply_promocode.times_used == apply_promocode.usage_limit:
                return "Promo Code applied is used up", 400

            promocodelog = PromoCodeLog.query.filter_by(customer_id=customer_id, promo_code_id=code_id).all()
            print(promocodelog)
            # print(len(promocodelog))
            if apply_promocode.usage_per_user < len(promocodelog):
                return "You have used the maximum limit of the applied Promo Code", 400
            
            cartitem = CartItem.query.filter_by(customer_id=customer_id).all()
            
            result = cart_items_schema.dump(cartitem)
            # print(result)
            for i in result:
                amount = i["amount"]
                cartitem_id = i["id"]
                update_cart_item = CartItem.query.get(cartitem_id)
                if apply_promocode.discount_type == "Percentage":
                    discounted_amount = (100-apply_promocode.discount)*amount/100
                    update_cart_item.discounted_amount = discounted_amount
                    db.session.commit()
                    return "Ok", 200
                elif apply_promocode.discount_type == "Price":
                    discounted_amount = (amount - apply_promocode.discount)
                    update_cart_item.discounted_amount = discounted_amount
                    db.session.commit()
                    return "Ok", 200
                else:
                    update_cart_item.discounted_amount = amount
                    db.session.commit()
                    return "Ok", 200
    if code_does_not_exist == False:
        return "Promo Code does not exist", 400                
        