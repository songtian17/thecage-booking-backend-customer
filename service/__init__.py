# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")  # config.py
app.config.from_pyfile("config.py")  # instance/config.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    return "Hello World!"

import service.routes.bookinghistory
import service.routes.calendar
import service.routes.checkout
import service.routes.customer
import service.routes.customerodoo
import service.routes.signin
import service.routes.signup
import service.routes.salesordercreate

# Now we can access the configuration variables via app.config["VAR_NAME"].
