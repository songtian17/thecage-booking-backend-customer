from service import app
from flask import request
import jwt


@app.route("/signin/", methods=["POST"])
def signin():
    req_data = request.get_json()

    login_username = req_data["username"]
    login_password = req_data["password"]

    file = open("instance/key.key", "rb")
    key = file.read()
    file.close()

    token = jwt.encode({"username": login_username}, key, algorithm="HS256")
    token = jwt.encode(
        {'username': login_username},
        key, algorithm='HS256'
    )

    return token
