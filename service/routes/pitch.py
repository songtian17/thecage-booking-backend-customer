from flask import jsonify
from service import app
from service.models import Pitch, pitch_schema, pitches_schema


# Get lists of Pitch
@app.route("/pitches", methods=["GET"])
def get_pitches():
    all_pitches = Pitch.query.all()
    result = pitches_schema.dump(all_pitches)
    return jsonify(result)

# Get pitch based on Id
@app.route("/pitch/<Id>", methods=["GET"])
def get_pitch_based_on_id(Id):
    pitch = Pitch.query.get(Id)
    return pitch_schema.jsonify(pitch)
