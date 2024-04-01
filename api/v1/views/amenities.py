#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    return:all states
    """
    amenity_list = []
    amenity_objct = storage.all("Amenity")
    for obj in amenity_objct.values():
        amenity_list.append(obj.to_json())

    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    create amenity route
    :return: newly created amenity obj
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    res = jsonify(new_amenity.to_json())
    res.status_code = 201

    return res


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    return: state obj with the specified id or error
    """

    fetch_objct = storage.get("Amenity", str(amenity_id))

    if fetch_objct is None:
        abort(404)

    return jsonify(fetch_objct.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: amenity object and 200 on success, or 400 or 404 on failure
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, 'Not a JSON')
    fetch_objct = storage.get("Amenity", str(amenity_id))
    if fetch_objct is None:
        abort(404)
    for key, val in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetch_objct, key, val)
    fetch_objct.save()
    return jsonify(fetch_objct.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    :param amenity_id: Amenity object id
    :return: empty dict with 200 or 404 if not found
    """

    fetch_objct = storage.get("Amenity", str(amenity_id))

    if fetch_objct is None:
        abort(404)

    storage.delete(fetch_objct)
    storage.save()

    return jsonify({})
