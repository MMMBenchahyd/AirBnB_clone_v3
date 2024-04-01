#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Return: response with json
    """
    data = {"status": "OK"}
    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "states": storage.count("State"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)

    return resp