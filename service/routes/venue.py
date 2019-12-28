from flask import jsonify
from service import app
from service.models import Venue, venue_schema, venues_schema, venue2s_schema

# Get lists of Venue
@app.route("/venue", methods=["GET"])
def get_venues():
    all_venues = Venue.query.all()

    result = venues_schema.dump(all_venues)
    return jsonify(result)


# Get Venue based on ID
@app.route("/venue/<Id>", methods=["GET"])
def get_venue(Id):
    venue = Venue.query.get(Id)
    return venue_schema.jsonify(venue)

# Get venue and field
@app.route("/venues", methods=["GET"])
def get_venuess():
    venue = Venue.query.order_by(Venue.id).all()
    results = venue2s_schema.dump(venue)
    return jsonify(results)
