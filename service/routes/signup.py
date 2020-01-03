from service import app
from flask import request, jsonify
from service.models import Customer, customer_schema, customer_schema2, CustomerOdoo, customer_odoo_schema, Venue, venue2s_schema
from instance.config import url, db as database, username, password
from service import db
import bcrypt
from sqlalchemy import exc
from parse import parse
import json
import xmlrpc.client


@app.route("/signup", methods=["POST"])
def signup():
    req_data = request.get_json()

    register_username = req_data["username"]
    register_password = req_data["password"]
    register_email = req_data["email"]
    register_phone = req_data["phone"]
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(register_password.encode("utf8"), salt)
        register_password = hashed_password.decode("utf8")
        new_customer = Customer(
            register_email, register_username, register_password, register_phone
        )
        db.session.add(new_customer)
        db.session.commit()
    except exc.IntegrityError as e:
        dupe_field = parse('duplicate key value violates unique constraint "{constraint}"\nDETAIL:  Key ({field})=({input}) already exists.\n', str(e.orig))["field"]
        print(dupe_field)
        return json.dumps({'message': f'{dupe_field} already exists'}), 400, {'ContentType': 'application/json'}

    common = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/common")
    uid = common.authenticate(database, username, password, {})
    models = xmlrpc.client.ServerProxy(f"{url}xmlrpc/2/object")
    odoo_customer_id = models.execute_kw(
        database,
        uid,
        password,
        "res.partner",
        "create",
        [
            {
                "name": register_username,
                "email": register_email,
                "phone": register_phone,
            }
        ],
    )

    venue = Venue.query.order_by(Venue.id).all()
    results = venue2s_schema.dump(venue)

    for result in results:
        new_customer_odoo = CustomerOdoo(new_customer.id, odoo_customer_id, result["id"])
        db.session.add(new_customer_odoo)
        db.session.commit()

    return customer_schema2.jsonify(new_customer)
