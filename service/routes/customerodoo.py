from flask import request, jsonify
from service import app
from service.models import CustomerOdoo, customer_odoo_schema, customer_odoos_schema

from service import db

# Create a CustomerOdoo
@app.route("/customerodoo", methods=["POST"])
def add_customer_odoo():
    customer_id = request.json["customerId"]
    odoo_id = request.json["odooId"]
    venue_id = request.json["venueId"]

    new_customer_odoo = CustomerOdoo(customer_id, odoo_id, venue_id)

    db.session.add(new_customer_odoo)
    db.session.commit()

    return customer_odoo_schema.jsonify(new_customer_odoo)


# Get lists of CustomerOdoo
@app.route("/customerodoo", methods=["GET"])
def get_customer_odoos():
    all_customer_odoos = CustomerOdoo.query.all()
    result = customer_odoos_schema.dump(all_customer_odoos)
    return jsonify(result)


# Get CustomerOdoo based on ID
@app.route("/customerodoo/<Id>", methods=["GET"])
def get_customer_odoo(Id):
    customer_odoo = CustomerOdoo.query.get(Id)
    return customer_odoos_schema.jsonify(customer_odoo)


# Update a CustomerOdoo
@app.route("/customerodoo/<Id>", methods=["PUT"])
def update_customer_odoo(Id):
    customer_odoo = CustomerOdoo.query.get(Id)

    customer_id = request.json["customerId"]
    odoo_id = request.json["odooId"]
    venue_id = request.json["venue"]

    customer_odoo.id = customer_id
    customer_odoo.odoo_id = odoo_id
    customer_odoo.venue_id = venue_id

    db.session.commit()

    return customer_odoo_schema.jsonify(customer_odoo)


# Delete CustomerOdoo
@app.route("/customerodoo/<Id>", methods=["DELETE"])
def delete_customer_odoo(Id):
    customer_odoo = CustomerOdoo.query.get(Id)
    db.session.delete(customer_odoo)
    db.session.commit()

    return customer_odoo_schema.jsonify(customer_odoo)
