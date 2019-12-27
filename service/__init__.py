# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from instance.config import sender_email, sender_password

from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True, template_folder="templates")
CORS(app, allow_headers='*')
app.config.from_object("config")  # config.py
app.config.from_pyfile("config.py")  # instance/config.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = sender_email,
    MAIL_PASSWORD = sender_password,
))

mail = Mail(app)


@app.route("/")
def index():
    return "Hello World!"

import service.routes.bookinghistory
import service.routes.calendar
import service.routes.checkout
import service.routes.customer
import service.routes.customerodoo
import service.routes.forgetpassword
import service.routes.signin
import service.routes.signup
import service.routes.salesordercreate
import service.routes.venue
import service.routes.announcement
import service.routes.customtimeslot

# Now we can access the configuration variables via app.config["VAR_NAME"].
