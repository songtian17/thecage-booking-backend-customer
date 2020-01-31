from service import app
import xmlrpc.client
import sys
import json
from service.models import Venue, Field, field_schema, fields_schema, fields2_schema, field3_schema, fields3_schema, Pitch
from instance.config import url, db, username, password
from flask import request
from datetime import datetime, timedelta


@app.route("/calendar/day", methods=["POST"])
def route1():
    model_result = ""
    req_data = request.get_json()

    booking_date = req_data["bookingDate"]
    booking_date_minus8 = datetime.strftime(datetime.strptime(booking_date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
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
                ["booking_start", ">=", booking_date_minus8],
                ["booking_end", "<=", booking_date_minus8],
                ["venue_id", "=", result["odoo_id"]],
            ]
        ],
        {"fields": ["id", "booking_start", "booking_end", "pitch_id"]},
    )
    for result in model_results:
        # print(result["pitch_id"][0])
        db_pitch = Pitch.query.filter_by(odoo_id=result["pitch_id"][0]).first()
        # print(db_pitch.odoo_id)
        result['booking_start'] = datetime.strftime(datetime.strptime(result['booking_start'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        result['booking_end'] = datetime.strftime(datetime.strptime(result['booking_end'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        result["pitch_id"] = db_pitch.odoo_id
    # print (model_results)
    return json.dumps(model_results)

@app.route("/calendar/week", methods=["POST"])
def route2():
    model_result = ""
    req_data = request.get_json()

    booking_date_start = req_data["bookingDateStart"]
    booking_date_start_minus8 = datetime.strftime(datetime.strptime(booking_date_start, '%Y-%m-%d %H:%M:%S') - timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
    booking_date_end = req_data["bookingDateEnd"]
    booking_date_end_minus8 = datetime.strftime(datetime.strptime(booking_date_end, '%Y-%m-%d %H:%M:%S') - timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
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
                ["booking_start", ">=", booking_date_start_minus8],
                ["booking_end", "<=", booking_date_end_minus8],
                ["venue_id", "=", result["odoo_id"]],
            ]
        ],
        {"fields": ["id", "booking_start", "booking_end", "pitch_id"]},
    )
    for result in model_results:
        # print(result["pitch_id"][0])
        db_pitch = Pitch.query.filter_by(odoo_id=result["pitch_id"][0]).first()
        # print(db_pitch.odoo_id)
        result['booking_start'] = datetime.strftime(datetime.strptime(result['booking_start'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        result['booking_end'] = datetime.strftime(datetime.strptime(result['booking_end'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
        result["pitch_id"] = db_pitch.odoo_id
    # print (model_results)
    return json.dumps(model_results)
