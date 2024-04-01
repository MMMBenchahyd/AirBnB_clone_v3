#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    get all amenities of a place
    :param place_id: amenity id
    :return: all amenities
    """
    fetch_objct = storage.get("Place", str(place_id))

    all_amenit = []

    if fetch_objct is None:
        abort(404)

    for obj in fetch_objct.amenities:
        all_amenit.append(obj.to_json())

    return jsonify(all_amenit)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def amenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity in a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    fetch_objct = storage.get("Place", place_id)
    count = 0

    for obj in fetch_objct.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetch_objct.amenities.remove(obj)
            else:
                fetch_objct.amenity_ids.remove(obj.id)
            fetch_objct.save()
            count = 1
            break

    if count == 0:
        abort(404)
    else:
        resp = jsonify({})
        resp.status_code = 201
        return resp


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """

    fetch_objct = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    count_amenity = None

    if not fetch_objct or not amenity_obj:
        abort(404)

    for obj in fetch_objct.amenities:
        if str(obj.id) == amenity_id:
            count_amenity = obj
            break

    if count_amenity is not None:
        return jsonify(count_amenity.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetch_objct.amenities.append(amenity_obj)
    else:
        fetch_objct.amenities = amenity_obj

    fetch_objct.save()

    res = jsonify(amenity_obj.to_json())
    res.status_code = 201

    return res
