from service.models import (
    PurchaseLog,
    PurchaseItem,
    purchase_log_schema,
    purchase_logs_schema,
    purchase_log2_schema,
    purchase_log2s_schema,
    purchase_item_schema,
    purchase_items_schema,
)
from flask import request, jsonify
from service import app
from datetime import datetime
from service import db


@app.route("/bookinghistory/<Id>", methods=["GET"])
def get_bookinghistory(Id):
    timestamp_now = datetime.now()
    purchaselog_ids = []
    purchaseitem_logids = []
    return_dict = {"logs": [], "items": []}

    purchase_log = (
        PurchaseLog.query.order_by(PurchaseLog.timestamp.desc())
        .filter_by(customer_id=Id)
        .all()
    )
    results_purchase_log = purchase_log2s_schema.dump(purchase_log)
    for result in purchase_log:
        purchaselog_ids.append(result.id)

    for log_id in purchaselog_ids:
        purchase_item = (
            PurchaseItem.query.order_by(PurchaseItem.id.desc())
            .filter_by(purchase_log_id=log_id)
            .filter(PurchaseItem.end_time > timestamp_now)
            .all()
        )
        results_purchase_item = purchase_items_schema.dump(purchase_item)
        for result in purchase_item:
            purchaseitem_logids.append(result.purchase_log_id)
        for i in results_purchase_item:
            return_dict["items"].append(i)

    for log_id in purchaseitem_logids:
        print (log_id)
        purchase_log = (
            PurchaseLog.query.order_by(PurchaseLog.timestamp.desc())
            .filter_by(customer_id=Id, id=log_id)
            .all()
        )
        results_purchase_log = purchase_log2s_schema.dump(purchase_log)
        for log in results_purchase_log:
            return_dict["logs"].append(log)

    return jsonify(return_dict)
    