from flask import render_template, jsonify, request
import paypalrestsdk
from service import app

paypalrestsdk.configure({
  "mode": "sandbox",  # sandbox or live
  "client_id": "ASA4ybdyLNfxxHHIqPRZCIMZglI-0K8e58wS6SVjsaapSZ-gS_nGVJbuZxYTvJ0kiTQogMya3iHbGH9p",
  "client_secret": "EFdDfOYOWBsCZwDHbmODAXI9o4b1886hNfvXx6Savr35rmEMQQqkVaWP5KuGGczzs-DsMSIkjcKqy5LM"})

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
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