from service import app
import xmlrpc.client
import sys
import json
from instance.config import url, db, username, password
from flask import request


@app.route("/calendar/day", methods=["POST"])
def route1():
    model_result = ""
    req_data = request.get_json()

    booking_date = req_data["bookingDate"]
    venue_name = req_data["venueName"]

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
                ["venue_id", "=", venue_name],
            ]
        ],
        {"fields": ["id", "booking_start", "booking_end", "pitch_id", "venue_id"]},
    )
    return json.dumps(model_results)
