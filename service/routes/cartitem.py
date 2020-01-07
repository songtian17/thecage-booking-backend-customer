from service import app
from flask import jsonify, request
from service.models import Venue, Field, CartItem, Product, Pitch, cart_item_schema, cart_items_schema, cart_item2s_schema, PromoCode
from datetime import datetime, timedelta
from service import db
import jwt
import json


# Create
@app.route("/cartitem", methods=["POST"])
def add_cartitem():
    tokenstr = request.headers["Authorization"]
    items = request.json["items"]
    for i in items:
        pitch_id = i["pitchId"]
        start_time = i["timeStart"]
        end_time = i["timeEnd"]
        expiry_date = datetime.now() + timedelta(minutes=20)
        product_id = i["productId"]   
        code_name = i.get("code")

        # venue = Venue.query.filter_by(name=venue_name).first()

        # venue_id = venue.id

        product = Product.query.get(product_id)
        amount = product.price

        # field = Field.query.filter_by(field_type=field_type, venue_id=venue_id).first()
        # field_id = field.id

        pitch = Pitch.query.get(pitch_id)
        new_pitch_id = pitch.id

        field_id = pitch.field_id
        field = Field.query.get(field_id)

        venue_id = field.venue_id

        promocode = PromoCode.query.filter_by(code=code_name).first()
        promocode_id = promocode.id

        if code_name is not None:
            promocode = PromoCode.query.filter_by(code=code_name).first()
            x = promocode.discount_type
            if x == "Percentage":
                discount_amount = (100-promocode.discount)*amount/100
            elif x == "Price":
                discount_amount = (amount - promocode.discount)
            else:
                discount_amount = amount

        file = open("instance/key.key", "rb")
        key = file.read()
        file.close()
        tokenstr = tokenstr.split(" ")
        token = tokenstr[1]
        customer_id = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]

        newcartitem = CartItem(venue_id, field_id, new_pitch_id, promocode_id, customer_id, start_time, end_time, expiry_date, product_id, amount, discount_amount)
        db.session.add(newcartitem)

    db.session.commit()
    return (request.json)

# Update
# @app.route("/cartitem/<Id>", methods=["PUT"])
# def update_cartitem(Id):
#     cartitem = CartItem.query.get(Id) 
#     product_name = request.json["product"]

    
#     product = Product.query.filter_by(name=product_name).first()
#     product_id = product.id
#     amount = product.price

#     code_id = cartitem.promocode_id
#     print(code_id)

#     if code_id is not None:
#         promocode = PromoCode.query.get(code_id)
#         x = promocode.discount_type
#         if x == "Percentage":
#             discount_amount = (100-promocode.discount)*amount/100
#         elif x == "Price":
#             discount_amount = (amount - promocode.discount)
#         else:
#             discount_amount = amount
#     else:
#         discount_amount = amount

#     cartitem.product_id = product_id
#     cartitem.discount_amount = discount_amount
#     cartitem.amount = amount

#     db.session.commit()

#     return cart_item_schema.jsonify(cartitem)

# Get customer's cart items
@app.route("/cartitem", methods=["GET"])
def get_cartitem():
    tokenstr = request.headers["Authorization"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    customerid = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]

    cartitems = CartItem.query.filter_by(customer_id=customerid).filter(CartItem.expiry_date > datetime.now()).all()
    result = cart_items_schema.dump(cartitems)
    return jsonify(result)

# Get all cart items
@app.route("/allcartitems", methods=["GET"])
def get_allcartitems():

    cartitems = CartItem.query.filter(CartItem.expiry_date > datetime.now()).all()
    result = cart_item2s_schema.dump(cartitems)
    return jsonify(result)

# Get cartitem by Id
@app.route("/cartitem/<Id>", methods=["GET"])
def get_cartitem_by_id(Id):
    cartitems = CartItem.query.get(Id)
    return cart_item_schema.jsonify(cartitems)

# Delete
@app.route("/cartitem/<Id>", methods=["DELETE"])
def delete_cartitem(Id):
    cartitem = CartItem.query.get(Id)
    db.session.delete(cartitem)
    db.session.commit()

    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})