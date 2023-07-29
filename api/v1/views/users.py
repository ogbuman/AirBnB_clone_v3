#!/usr/bin/python3
"""users api views
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def get_all_users():
    """ get all users
    """
    users_list = []
    users = storage.all(User)

    for user in users.values():
        users_list.append(user.to_dict())

    return jsonify(users_list), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_users_id(user_id):
    """ get user by id

    Args:
        user_id (str): User Id
    """

    user = storage.get("User", str(user_id))
    if not user:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ delete a user

    Args:
        user_id (str): user id
    """

    user = storage.get("User", str(user_id))

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """creates a new user
    """

    params_json = request.get_json()

    if not params_json:
        abort(400, "Not a JSON")

    if "email" not in params_json:
        abort(400, "Missing email")
    if "password" not in params_json:
        abort(400, "Missing password")

    new_user = User(**params_json)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update a user

    Args:
        user_id (str): User id to alter
    """
    # get user object to update
    user = storage.get("User", str(user_id))

    if not user:
        abort(404)

    # get params from put hhtp method
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")

    for k, v in params_json.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, k, v)

    user.save()

    return jsonify(user.to_dict()), 200
