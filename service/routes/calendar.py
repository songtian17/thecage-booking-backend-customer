from service import app
import xmlrpc.client
import sys
import json
from service.models import Venue, Field, field_schema, fields_schema, fields2_schema, field3_schema, fields3_schema, Pitch
from instance.config import url, db, username, password
from flask import request


@app.route("/calendar/day", methods=["POST"])
def route1():
    model_result = ""
    req_data = request.get_json()

    booking_date = req_data["bookingDate"]
    field_id = req_data["fieldId"]

    result_fields = Field.query.filter_by(id=field_id).first()
    result = field3_schema.dump(result_fields)
    common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")

    model_results = models.execute_kw(
        db,
        uid,
        password,
        "sale.order.line",
        "search_read",
        [
            [
                ["booking_start", ">=", booking_date],
                ["booking_end", "<=", booking_date],
                ["venue_id", "=", result["odoo_id"]],
            ]
        ],
        {"fields": ["id", "booking_start", "booking_end", "pitch_id", "venue_id"]},
    )
    # for model_result in model_results:
    #     print(model_result, file=sys.stdout)
    return json.dumps(model_results)
