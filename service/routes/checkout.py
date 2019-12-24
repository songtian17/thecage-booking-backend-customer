from service.models import PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


@app.route("/checkout", methods=["POST"])
def checkout():
    customer_id = request.json["customerId"]
    timestamp = datetime.now()
    new_purchase_log = PurchaseLog(customer_id, timestamp)

    db.session.add(new_purchase_log)
    db.session.flush()
    purchaselog_id = new_purchase_log.id

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
