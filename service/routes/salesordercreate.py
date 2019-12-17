from service import app
import xmlrpc.client
import sys
import json
import datetime
from datetime import timedelta
from instance.config import url, db, username, password, id
from service.models import Admin, CustomerOdoo, customer_odoo_schema, customer_odoos_schema
from flask import request, jsonify


@app.route("/salesorder/create", methods=["POST"])
def salesordercreate():
    model_result = ""

    common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")

    req_data = request.get_json()

    input_customer_id = req_data["customerId"]
    customer_odoo = CustomerOdoo.query.filter_by(customer_id=input_customer_id).first()
    customer_odoo_odoo_id = customer_odoo.odoo_id

    print (id)

    currentDT = datetime.datetime.now()-timedelta(hours=8)
    model_results = models.execute_kw(
        db,
        uid,
        password,
        "sale.order",
        "create",
        [
            {
                "date_order": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                "partner_id": int(customer_odoo_odoo_id),
                "user_id": int(id),
            }
        ],
    )

    return json.dumps(model_results)
