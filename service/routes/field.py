from flask import request, jsonify
from service import app
from service.models import Venue, Field, field_schema, fields_schema, fields2_schema, field2_schema, fields3_schema, Pitch, pitches_schema
from datetime import datetime
from sqlalchemy import exc
import json
from service import db

# Create new Field
@app.route("/field/<Id>", methods=['POST'])
def add_field(Id):
    try:
        venue = Venue.query.get(Id)
        venue_id = venue.id
        odoo_id = request.json["odooId"]
        name = request.json["name"]
        field_type = request.json["fieldType"]
        colour = request.json["colour"]
        num_pitches = request.json["numPitches"]
        created_at = datetime.now()
        updated_at = datetime.now()

        new_field = Field(name, venue_id, field_type, num_pitches, colour, created_at, updated_at, odoo_id)
        db.session.add(new_field)
        db.session.commit()
        if int(num_pitches) >= 1:
            for i in range(int(num_pitches)):
                field_id = new_field.id
                pitchname = "P" + str(i+1)
                odoo_id = None
                new_pitch = Pitch(pitchname, field_id, odoo_id)
                db.session.add(new_pitch)
        db.session.commit()
    except exc.IntegrityError:
        return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


# # Get lists of Field

# @app.route("/field", methods=["GET"])
# def get_fields():
#     all_fields = Field.query.all()
#     result = fields_schema.dump(all_fields)
#     return jsonify(result)


# # Get field and Pitch based on field ID
# @app.route("/fields/<field_id>", methods=["GET"])
# def get_pitch_based_on_field_id(field_id):
#     all_pitches = Pitch.query.filter_by(field_id=field_id).all()
#     result = pitches_schema.dump(all_pitches)
#     return pitches_schema.jsonify(result)


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

# Update a Field
@app.route("/field/<Id>", methods=["PUT"])
def update_field(Id):
    try:
        field = Field.query.get(Id)

        name = request.json["name"]
        field_type = request.json["fieldType"]
        colour = request.json["colour"]
        updatedat = datetime.now()

        field.name = name
        field.field_type = field_type
        field.colour = colour
        field.updatedat = updatedat

        db.session.commit()
    except exc.IntegrityError:
        return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})

# Delete Field
@app.route("/field/<Id>", methods=["DELETE"])
def delete_field(Id):
    field = Field.query.get(Id)

    db.session.delete(field)
    db.session.commit()

    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})
