from service.models import PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema, PromoCodeLog, PromoCode
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db
import jwt


@app.route("/checkout", methods=["POST"])
def checkout():
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    customer_id = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]

    timestamp = datetime.now()
    new_purchase_log = PurchaseLog(customer_id, timestamp)

    db.session.add(new_purchase_log)
    db.session.flush()
    purchaselog_id = new_purchase_log.id
    code = request.json.get("promoCode")
    if code is None:
        print("no promo code") 
    else:
        promocode = PromoCode.query.filter_by(code=code).first()
        promocode_id = promocode.id
        promocode.times_used += 1
        new_promo_code_log = PromoCodeLog(timestamp, promocode_id, customer_id)
        db.session.add(new_promo_code_log)
        db.session.commit()

    items = request.json["items"]
    for i in items:
        purchase_log_id = purchaselog_id
        product_id = i["productId"]
        field_id = i["fieldId"]
        pitch_id = i["pitchId"]
        price = i["price"]
        start_time = i["startTime"]
        end_time = i["endTime"]
        new_purchase_item = PurchaseItem(purchase_log_id, product_id, field_id, pitch_id, price, start_time, end_time)
        db.session.add(new_purchase_item)

    db.session.commit()

    return (request.json)
