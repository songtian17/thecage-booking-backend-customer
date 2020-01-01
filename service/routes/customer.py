from flask import request, jsonify
from service import app
from service.models import Customer, customer_schema, customers_schema
import bcrypt
import json
from service import db
from parse import parse
from sqlalchemy import exc

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
    password = request.json.get("newPassword")
    old_password = request.json.get("oldPassword")
    email = request.json["email"]
    name = request.json["name"]
    phone_no = request.json["phoneNo"]

    if password is None:
        customer.email = email
        customer.name = name
        customer.phone_no = phone_no
        db.session.commit()
    else:
        password = request.json["newPassword"]
        old_password = request.json["oldPassword"]

        if bcrypt.checkpw(
            old_password.encode("utf-8"), customer.password.encode("utf-8")
        ):
            try:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode("utf8"), salt)
                password_decoded = hashed_password.decode("utf8")

                customer.email = email
                customer.password = password_decoded
                customer.name = name
                customer.phone_no = phone_no
                db.session.commit()
            except exc.IntegrityError as e:
                dupe_field = parse('duplicate key value violates unique constraint "{constraint}"\nDETAIL:  Key ({field})=({input}) already exists.\n', str(e.orig))["field"]
                print(dupe_field)
                return json.dumps({'message': f'{dupe_field} already exists'}), 400, {'ContentType': 'application/json'}

        else:
            return json.dumps({'message': 'Passwords do not match'}), 400, {'ContentType': 'application/json'}

    return customer_schema.jsonify(customer)


# Delete Customer
@app.route("/customer/<Id>", methods=["DELETE"])
def delete_customer(Id):
    customer = Customer.query.get(Id)
    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)
