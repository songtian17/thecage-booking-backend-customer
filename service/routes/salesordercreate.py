from service import app
import xmlrpc.client
import sys
import json
import datetime
from instance.config import url, db, username, password
from service.models import CustomerOdoo, customer_odoo_schema, customer_odoos_schema
from flask import request, jsonify


@app.route("/salesorder/create", methods=["POST"])
def salesordercreate():
    model_result = ""
    req_data = request.get_json()

    input_customer_id = req_data["customerId"]
    input_admin_id = req_data["adminId"]

    customer_odoo = CustomerOdoo.query.get(input_customer_id)
    customer_id = customer_odoo.odoo_id

    common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")

    currentDT = datetime.datetime.now()
    print(currentDT.strftime("%Y-%m-%d %H:%M:%S"))

    model_results = models.execute_kw(
        db,
        uid,
        password,
        "sale.order",
        "create",
        [
            {
                # "campaign_id":"false",
                # "categ_ids":[["6","false",[]]],
                "categ_ids": [],
                # "client_order_ref":"false",
                "date_order": currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                # "fiscal_position":"false",
                # "incoterm":"false",
                # "medium_id":"false",
                # "message_follower_ids":'false',
                "message_follower_ids": [
                    [
                        "17541",
                        "4192",
                        "10243",
                        "10244",
                        "10245",
                        "5288",
                        "15498",
                        "15499",
                        "15500",
                        "17",
                        "6130",
                        "10111",
                        "6133",
                        "6134",
                        "6135",
                        "6137",
                        "6138",
                        "6139",
                        "6141",
                        "6142",
                        "6143",
                    ]
                ],
                # "message_ids":"false",
                "message_ids": [["852511", "852510"]],
                "note": "This is a computer generated bill and no signature is required. \n\nNo receipt will be issued unless specially requested. \n\nYou may want to print this booking confirmation and bring it along during the day of play. \n\nPlease call us at 63449345 or email us at iwannaplay@thecage.com.sg for any other enquiries. ",
                "order_line": [],
                "order_policy": "manual",
                # "origin":"false",
                "partner_id": int(customer_id),
                "partner_invoice_id": int(customer_id),
                "partner_shipping_id": int(customer_id),
                # "payment_term":"false",
                # "paypal_payment_info":"false",
                "picking_policy": "direct",
                "pricelist_id": "1",
                # "project_id":"false",
                "qr_in_report": "true",
                # "sale_due_date":"false",
                # "section_id":"false",
                # "source_id":"false",
                "user_id": int(input_admin_id),
                "warehouse_id": "3",
            }
        ],
    )

    return json.dumps(model_results)
