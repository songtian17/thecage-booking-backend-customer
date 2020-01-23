from flask import render_template, jsonify, request
import paypalrestsdk
from service import app
from service.models import Venue, Field, Pitch, Product, CartItem, cart_items_schema
import jwt

paypalrestsdk.configure({
  "mode": "sandbox",  # sandbox or live
  "client_id": "ASA4ybdyLNfxxHHIqPRZCIMZglI-0K8e58wS6SVjsaapSZ-gS_nGVJbuZxYTvJ0kiTQogMya3iHbGH9p",
  "client_secret": "EFdDfOYOWBsCZwDHbmODAXI9o4b1886hNfvXx6Savr35rmEMQQqkVaWP5KuGGczzs-DsMSIkjcKqy5LM"})

@app.route('/payment', methods=['POST'])
def payment():
    tokenstr = request.headers["Authorization"]    
    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()
    tokenstr = tokenstr.split(" ")
    token = tokenstr[1]
    customer_id = jwt.decode(token, key, algorithms=['HS256'])["customer_id"]

    items_list = []
    cartitem = CartItem.query.filter_by(customer_id=customer_id).all()
    results = cart_items_schema.dump(cartitem)
    # print(results)
    total_amount = 0
    for result in results:
        item = {}
        product = Product.query.get(result["product_id"])
        item["name"] = product.name
        item["sku"] = product.id
        item["price"] = result["discounted_amount"]
        item["description"] = f'{result["venue_id"]}{result["field_id"]}{result["pitch_id"]}{result["start_time"]}{result["end_time"]}'
        item["currency"] = "SGD"
        item["quantity"] = 1
        items_list.append(item)
        total_amount += result["discounted_amount"]
    print(items_list)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": items_list},
                # "items": [{
                #     "name": "testitem",
                #     "sku": "12345",
                #     "price": "10.00",
                #     "description": "",
                #     "currency": "SGD",
                #     "quantity": 1}]},
            "amount": {
                "total": str(total_amount),
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success': success})