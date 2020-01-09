from flask import jsonify
from service import app
from service.models import Venue, venue2_schema, venue2s_schema, Field, fields3_schema


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
