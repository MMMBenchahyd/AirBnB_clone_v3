#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    retrieves all Place objects by city
    :return: json of all Places
    """
    plc_list = []
    city_objct = storage.get("City", str(city_id))
    for obj in city_objct.places:
        plc_list.append(obj.to_json())

    return jsonify(plc_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    create place route
    :return: newly created Place obj
    """
    plc_json = request.get_json(silent=True)
    if plc_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", plc_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in plc_json:
        abort(400, 'Missing user_id')
    if "name" not in plc_json:
        abort(400, 'Missing name')

    plc_json["city_id"] = city_id

    new_place = Place(**plc_json)
    new_place.save()
    res = jsonify(new_place.to_json())
    res.status_code = 201

    return res


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    gets a specific Place object by ID
    :param place_id: place object id
    :return: place obj with the specified id or error
    """

    fetched_objct = storage.get("Place", str(place_id))

    if fetched_objct is None:
        abort(404)

    return jsonify(fetched_objct.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    updates specific Place object by ID
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    plc_json = request.get_json(silent=True)

    if plc_json is None:
        abort(400, 'Not a JSON')

    fetched_objct = storage.get("Place", str(place_id))

    if fetched_objct is None:
        abort(404)

    for key, val in plc_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_objct, key, val)

    fetched_objct.save()

    return jsonify(fetched_objct.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    deletes Place by id
    :param place_id: Place object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_objct = storage.get("Place", str(place_id))

    if fetched_objct is None:
        abort(404)

    storage.delete(fetched_objct)
    storage.save()

    return jsonify({})
