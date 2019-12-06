from service import app
from flask import request
import bcrypt
import json


@app.route("/signup/", methods=["POST"])
def signup():
    req_data = request.get_json()

    register_username = req_data["username"]
    register_password = req_data["password"]
    register_email = req_data["email"]
    register_phone = req_data["phone"]

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(register_password.encode("utf8"), salt)
    print("hashed pw", hashed_password)

    file = open("instance/hashedpw.txt", "w+")
    file.write(hashed_password.decode("utf-8"))
    file.close()

    new_customer = {}
    new_customer["customer"] = []
    new_customer["customer"].append(
        {
            "username": register_username,
            "email": register_email,
            "password": hashed_password.decode("utf-8"),
            "phone": register_phone,
        }
    )

    with open("instance/customers.txt", "w") as outfile:
        json.dump(new_customer, outfile)

    return new_customer
