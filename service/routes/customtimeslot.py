from flask import jsonify
from service import app
from service.models import CustomTimeSlot, customtimeslot_schema, customtimeslots_schema
from service import db

# Get customtimeslot based on Id
@app.route("/customtimeslot/<Id>", methods=["GET"])
def get_customtimeslot_based_on_id(Id):
    customtimeslot = CustomTimeSlot.query.get(Id)

    return customtimeslot_schema.jsonify(customtimeslot)


# Get list of customtimeslots based on field id
@app.route("/customtimeslots/<field_id>", methods=["GET"])
def get_customtimeslot(field_id):
    all_customtimeslot = CustomTimeSlot.query.filter_by(field_id=field_id).all()
    result = customtimeslots_schema.dump(all_customtimeslot)
    return jsonify(result)

# Delete Custom Timeslot
@app.route("/customtimeslot/<Id>", methods=["DELETE"])
def delete_customtimeslot(Id):
    customtimeslot = CustomTimeSlot.query.get(Id)

    db.session.delete(customtimeslot)
    db.session.commit()

    return customtimeslot_schema.jsonify(customtimeslot)
