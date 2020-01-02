from flask import request, jsonify
from service import app
from service.models import Venue, venue_schema, venues_schema, venue2_schema, venue2s_schema, Field, fields3_schema
from datetime import datetime
from sqlalchemy import exc
import json
from service import db

# Create new Venue
@app.route("/venue", methods=['POST'])
def add_venue():
    try:
        name = request.json["name"]
        created_at = datetime.now()
        updated_at = datetime.now()
        new_venue = Venue(name, created_at, updated_at)

        db.session.add(new_venue)
        db.session.commit()
    except exc.IntegrityError:
        return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})


# # Get lists of Venue
# @app.route("/venue", methods=["GET"])
# def get_venues():
#     all_venues = Venue.query.all()

#     result = venues_schema.dump(all_venues)
#     return jsonify(result)


# Get lists of Fields based on Venue ID
@app.route("/venues/<venue_id>", methods=["GET"])
def get_fields_based_on_venue_id(venue_id):
    all_fields = Field.query.filter_by(venue_id=venue_id).all()
    result = fields3_schema.dump(all_fields)
    return fields3_schema.jsonify(result)

# Get Venue based on ID
@app.route("/venue/<Id>", methods=["GET"])
def get_venue(Id):
    venue = Venue.query.get(Id)
    return venue2_schema.jsonify(venue)


# Get list of venues
@app.route("/venues", methods=["GET"])
def get_venuess():
    venue = Venue.query.order_by(Venue.id).all()
    results = venue2s_schema.dump(venue)
    return jsonify(results)
    # venue_fields = Venue.query.join(Field, Venue.id == Field.venue_id).add_column().all()
    # # result = venue2s_schema().dump(venue_fields)
    # # return jsonify(result)
    # return venue_fields
# Update a Venue
@app.route("/venue/<Id>", methods=['PUT'])
def update_venue(Id):
    try:
        venue = Venue.query.get(Id)

        name = request.json["name"]
        updatedat = datetime.now()
        venue.name = name
        venue.updateat = updatedat

        db.session.commit()
    except exc.IntegrityError:
        return json.dumps({'message': "Name '" + name + "' already exists"}), 400, {'ContentType': 'application/json'}
    return (json.dumps({'message': 'success'}), 200, {'ContentType': 'application/json'})

# Delete Venue
@app.route("/venue/<Id>", methods=["DELETE"])
def delete_venue(Id):
    venue = Venue.query.get(Id)
    db.session.delete(venue)
    db.session.commit()

    return venue_schema.jsonify(venue)
