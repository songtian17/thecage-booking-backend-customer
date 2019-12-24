from service.models import PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


@app.route("/bookinghistory", methods=["GET"])
def get_bookinghistory():

    purchase_log = PurchaseLog.query.order_by(PurchaseLog.timestamp.desc()).all()
    results_purchase_log = purchase_log2s_schema.dump(purchase_log)

    timestamp_now = datetime.now()

    purchase_item = PurchaseItem.query.order_by(PurchaseItem.id.desc()).filter(PurchaseItem.end_time>timestamp_now).all()
    results_purchase_item = purchase_items_schema.dump(purchase_item)

    return_dict = {'logs': [], 'items': []}
    for i in results_purchase_log:
        return_dict['logs'].append(i)
    for i in results_purchase_item:
        return_dict['items'].append(i)
    return (jsonify(return_dict))
