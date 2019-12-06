from service import app
from flask import request
import bcrypt
import jwt
import json


@app.route("/signin/", methods=["POST"])
def signin():

    req_data = request.get_json()

    login_username = req_data["username"]
    login_password = req_data["password"]
    hashed_password = ""

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()

    with open("instance/customers.txt") as json_file:
        data = json.load(json_file)
        for p in data["customer"]:
            if p["username"] == login_username:
                hashed_password = p["password"]
                if bcrypt.checkpw(
                    login_password.encode("utf-8"),
                    hashed_password.encode("utf-8")
                ):
                    token = jwt.encode(
                        {"username": login_username}, key, algorithm="HS256"
                    )
                    return token

    return "Login Failed", 401
