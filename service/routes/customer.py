from flask import request, jsonify
from service import app
from service.models import Customer, customer_schema, customers_schema

from service import db

# Create a Customer
@app.route("/customer", methods=["POST"])
def add_customer():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    phone_no = request.json["phone_no"]

    new_customer = Customer(email, password, name, phone_no)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)


# Get lists of Customer
@app.route("/customer", methods=["GET"])
def get_customers():
    all_admins = Customer.query.all()
    result = customers_schema.dump(all_admins)
    return jsonify(result)


# Get Customer based on ID
@app.route("/customer/<Id>", methods=["GET"])
def get_customer(Id):
    customer = Customer.query.get(Id)
    return customer_schema.jsonify(customer)


# Update a Customer
@app.route("/customer/<Id>", methods=["PUT"])
def update_customer(Id):
    customer = Customer.query.get(Id)

    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    phone_no = request.json["phone_no"]

    customer.email = email
    customer.password = password
    customer.name = name
    customer.phone_no = phone_no

    db.session.commit()

    return customer_schema.jsonify(customer)


# Delete Customer
@app.route("/customer/<Id>", methods=["DELETE"])
def delete_customer(Id):
    customer = Customer.query.get(Id)
    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)
