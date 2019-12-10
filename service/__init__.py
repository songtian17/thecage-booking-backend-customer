# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")  # config.py
app.config.from_pyfile("config.py")  # instance/config.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


@app.route("/")
def index():
    return "Hello World!"

import service.routes.calendar
import service.routes.signin
import service.routes.signup

# Now we can access the configuration variables via app.config["VAR_NAME"].
