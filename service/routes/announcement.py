from flask import jsonify
from service import app
from service.models import Announcement, announcement2_schema, announcement2s_schema


# Get announcement
@app.route("/announcement", methods=["GET"])
def get_announcement():
    all_announcement = Announcement.query.all()
    result = announcement2s_schema.dump(all_announcement)
    return jsonify(result)

# Get announcement by Id
@app.route("/announcement/<Id>", methods=["GET"])
def get_announcement_by_id(Id):
    announcement = Announcement.query.get(Id)
    return announcement2_schema.jsonify(announcement)