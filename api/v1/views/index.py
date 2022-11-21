#!/usr/bin/python3
"""Script creates a route that returns status in JSON format."""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
	"""show the status function"""
	return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """return number of stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
