from service.models import Field, PurchaseLog, PurchaseItem, purchase_log_schema, purchase_logs_schema, purchase_log2_schema, purchase_log2s_schema, purchase_item_schema, purchase_items_schema, PromoCodeLog, PromoCode, Product, product_schema, products_schema, CustomerOdoo
from flask import request, jsonify
from service import app, db
from datetime import datetime, timedelta
import jwt
import xmlrpc.client
import json
from instance.config import url, db as database, username, password, id


# @app.route("/paypal", methods=["POST"])
# def paypal():


@app.route("/checkout", methods=["POST"])
def checkout():
    # assign variables
    tokenstr = request.headers["Authorization"]
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    customer_id = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]
    timestamp = datetime.now()
    timestamp_utc = datetime.now()-timedelta(hours=8)
    common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
    uid = common.authenticate(database, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")
    model_results = ""
    customer_odoo = CustomerOdoo.query.filter_by(customer_id=customer_id).first()
    customer_odoo_odoo_id = customer_odoo.odoo_id

    # to clean

    # create purchase log in postgres
    new_purchase_log = PurchaseLog(customer_id, timestamp)
    db.session.add(new_purchase_log)
    db.session.flush()
    db.session.commit()
    purchaselog_id = new_purchase_log.id

    # create purchase log in odoo
    sales_order_id = models.execute_kw(
        database,
        uid,
        password,
        "sale.order",
        "create",
        [
            {
                "date_order": timestamp_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "partner_id": int(customer_odoo_odoo_id),
                "user_id": int(id),
            }
        ],
    )

    # check and/or update promo code usage
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

    # purchase item
    items = request.json["items"]
    for i in items:
        # create in postgres
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

        # assigning more variables
        product_qty = (datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')).total_seconds()/3600
        booking_start = datetime.strftime(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')-timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        booking_end = datetime.strftime(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')-timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        product_name = (Product.query.get(product_id)).name
        product_odoo_id = (Product.query.get(product_id)).odoo_id
        venue_id = (Field.query.get(field_id)).venue_id

        # create in odoo
        model_results = models.execute_kw(
            database,
            uid,
            password,
            "sale.order.line",
            "create",
            [
                {
                    "product_uos_qty": product_qty,
                    "product_uom_qty": product_qty,
                    "booking_start": booking_start,
                    "booking_end": booking_end,
                    "name": product_name,
                    "order_id": int(sales_order_id),
                    "product_id": int(product_odoo_id),
                    "pitch_id": int(pitch_id),
                    "venue_id": int(venue_id),
                    "booking_state": "in_progress",
                    "partner_id": int(customer_odoo_odoo_id)
                },
            ],
            {
                "context": {
                    "tz": "Singapore"
                }
            }
        )
        print(json.dumps(model_results))

    return (request.json)
