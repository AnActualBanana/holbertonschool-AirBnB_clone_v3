#!/usr/bin/python3
"""Script creates a route that returns status in JSON format."""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    "/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def places(city_id):
    """method retrieves list of all Place objects in a given city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place(place_id):
    """method retrieves a Place object in JSON format"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """method deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """method creates a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    elif 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user = storage.get(User, request.json['user_id'])
    if user is None:
        abort(404)
    elif 'name' not in request.json:
        abort(400, 'Missing name')
    new_place = Place(**request.get_json())
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """method updates an existing Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif not request.json or not request.is_json:
        abort(400, 'Not a JSON')
    else:
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
