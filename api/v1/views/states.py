#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: json of all states
    """
    state_list = []
    state_obj = storage.all("State")
    for objct in state_obj.values():
        state_list.append(objct.to_json())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    return: newly created state obj
    """
    stat_j = request.get_json(silent=True)
    if stat_j is None:
        abort(400, 'Not a JSON')
    if "name" not in stat_j:
        abort(400, 'Missing name')

    new_state = State(**stat_j)
    new_state.save()
    res = jsonify(new_state.to_json())
    res.status_code = 201

    return res


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    return: state obj with the specified id or error
    """

    fetch_objct = storage.get("State", str(state_id))

    if fetch_objct is None:
        abort(404)

    return jsonify(fetch_objct.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    return: state object and 200 on success, or 400 or 404 on failure
    """
    stat_j = request.get_json(silent=True)
    if stat_j is None:
        abort(400, 'Not a JSON')
    fetch_objct = storage.get("State", str(state_id))
    if fetch_objct is None:
        abort(404)
    for k, value in stat_j.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(fetch_objct, k, value)
    fetch_objct.save()
    return jsonify(fetch_objct.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    return: empty dict with 200 or 404 if not found
    """

    fetch_objct = storage.get("State", str(state_id))

    if fetch_objct is None:
        abort(404)

    storage.delete(fetch_objct)
    storage.save()

    return jsonify({})
