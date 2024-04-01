#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    retrieves all User objects
    :return: json of all users
    """
    user_l = []
    user_objct = storage.all("User")
    for obj in user_objct.values():
        user_l.append(obj.to_json())

    return jsonify(user_l)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    create user route
    :return: newly created user obj
    """
    usr_json = request.get_json(silent=True)
    if usr_json is None:
        abort(400, 'Not a JSON')
    if "email" not in usr_json:
        abort(400, 'Missing email')
    if "password" not in usr_json:
        abort(400, 'Missing password')

    new_usr = User(**usr_json)
    new_usr.save()
    res = jsonify(new_usr.to_json())
    res.status_code = 201

    return res


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    gets a specific User object by ID
    :param user_id: user object id
    :return: user obj with the specified id or error
    """

    fetch_objct = storage.get("User", str(user_id))

    if fetch_objct is None:
        abort(404)

    return jsonify(fetch_objct.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    updates specific User object by ID
    :param user_id: user object ID
    :return: user object and 200 on success, or 400 or 404 on failure
    """
    usr_json = request.get_json(silent=True)

    if usr_json is None:
        abort(400, 'Not a JSON')

    fetch_objct = storage.get("User", str(user_id))

    if fetch_objct is None:
        abort(404)

    for key, val in usr_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetch_objct, key, val)

    fetch_objct.save()

    return jsonify(fetch_objct.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    deletes User by id
    :param user_id: user object id
    :return: empty dict with 200 or 404 if not found
    """

    fetch_objct = storage.get("User", str(user_id))

    if fetch_objct is None:
        abort(404)

    storage.delete(fetch_objct)
    storage.save()

    return jsonify({})
