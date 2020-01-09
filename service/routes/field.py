from flask import jsonify
from service import app
from service.models import Field, fields2_schema, field2_schema


# Get list of fields
@app.route("/fields", methods=["GET"])
def get_fieldss():
    field = Field.query.order_by(Field.id).all()
    results = fields2_schema.dump(field)
    return jsonify(results)


# Get field based on Id
@app.route("/field/<Id>", methods=["GET"])
def get_fields_based_on_id(Id):
    field = Field.query.get(Id)

    return field2_schema.jsonify(field)


    



