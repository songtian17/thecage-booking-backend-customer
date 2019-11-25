# app.py or app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return "Hello World!"

import service.routes.route1
import service.routes.route2

# Now we can access the configuration variables via app.config["VAR_NAME"].