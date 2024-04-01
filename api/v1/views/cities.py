#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    ct_list = []
    stat_objct = storage.get("State", state_id)

    if stat_objct is None:
        abort(404)
    for obj in stat_objct.cities:
        ct_list.append(obj.to_json())

    return jsonify(ct_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    c_json = request.get_json(silent=True)
    if c_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in c_json:
        abort(400, 'Missing name')

    c_json["state_id"] = state_id

    new_c = City(**c_json)
    new_c.save()
    res = jsonify(new_c.to_json())
    res.status_code = 201

    return res


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    fetch_objct = storage.get("City", str(city_id))

    if fetch_objct is None:
        abort(404)

    return jsonify(fetch_objct.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    c_json = request.get_json(silent=True)
    if c_json is None:
        abort(400, 'Not a JSON')
    fetch_objct = storage.get("City", str(city_id))
    if fetch_objct is None:
        abort(404)
    for key, val in c_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetch_objct, key, val)
    fetch_objct.save()
    return jsonify(fetch_objct.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """

    fetch_objct = storage.get("City", str(city_id))

    if fetch_objct is None:
        abort(404)

    storage.delete(fetch_objct)
    storage.save()

    return jsonify({})
