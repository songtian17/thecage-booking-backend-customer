from service import app, db, mail
from flask import request, abort, render_template, url_for
from flask_mail import Message
from service.models import Customer, customer_schema, customers_schema
import bcrypt
import jwt
import json
from itsdangerous import URLSafeTimedSerializer, exc
from instance.config import sender_email


@app.route("/forget", methods=["POST"])
def forget():

    req_data = request.get_json()

    input_email = req_data["email"]
    try:
        customer = Customer.query.filter_by(email=input_email).first_or_404()
    except:
        abort(400)
    print(customer.email)
    send_reset_email(customer.email)
    return json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'}


def send_reset_email(email):
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    password_reset_serializer = URLSafeTimedSerializer(key)

    password_reset_url = url_for(
        'reset',
        token=password_reset_serializer.dumps(email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        "emailpasswordreset.html",
        password_reset_url=password_reset_url)

    msg = Message(
        "Request password reset",
        sender=sender_email,
        recipients=[email])
    msg.html = html
    mail.send(msg)
    print(password_reset_url)
    return json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'}


@app.route("/reset", methods=["GET", 'POST'])
def reset():
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    token = request.args.get('token')
    try:
        password_reset_serializer = URLSafeTimedSerializer(key)
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except exc.SignatureExpired:
        return json.dumps({'message': 'Expired link'}), 400, {'ContentType': 'application/json'}
    except exc.BadTimeSignature:
        return json.dumps({'message': 'Invalid link'}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


@app.route("/resetpassword/<Id>", methods=["PUT"])
def reset_password(Id):
    customer = Customer.query.get(Id)

    new_password = request.json["password"]

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_password.encode("utf8"), salt)
    new_hashed_password = hashed_password.decode("utf8")

    customer.password = new_hashed_password
    db.session.commit()

    return customer_schema.jsonify(customer)
