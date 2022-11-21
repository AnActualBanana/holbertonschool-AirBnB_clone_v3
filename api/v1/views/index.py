#!/usr/bin/python3
"""Script creates a route that returns status in JSON format."""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
	"""method shows the status of the API in JSON format"""
	return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """method calls count method of storage to show number of objects"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
