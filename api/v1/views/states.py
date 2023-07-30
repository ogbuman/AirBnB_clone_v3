#!/usr/bin/python3
""" States api views
"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


# Get method for read
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Gets all states
    """
    save_list = []
    result = storage.all(State)
    for values in result.values():
        save_list.append(values.to_dict())

    return jsonify(save_list), 200


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_id(state_id):
    """ Gets states by id
    """
    # get result for the class by its id using the
    # get method from storages
    result = storage.get("State", str(state_id))
    # check if no match, abort and return 404
    if result is None:
        abort(404)
    else:
        return jsonify(result.to_dict()), 200

# api delete route


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state

    Args:
        state_id (str): The state id
    """
    # get state
    result = storage.get("State", state_id)
    # check if exist
    if result is None:
        abort(404)

    # delete and save
    storage.delete(result)
    storage.save()

    # return empty dict with status code 200
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates new state objects
    """
    # get dict params from post
    params_json = request.get_json(silent=True)
    # if not json
    if params_json is None:
        abort(400, "Not a JSON")
    if "name" not in params_json:
        abort(400, "Missing name")

    # create a new state instance with the params key, values
    new_state = State(**params_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """ Updates a state

    Args:
        state_id (str): state id
    """
    # get dict params from put request
    params_json = request.get_json(silent=True)
    # if not json
    if params_json is None:
        abort(400, "Not a JSON")
    # get the state with the passed id
    result = storage.get("State", str(state_id))
    if result is None:
        abort(404)

    for k, v in params_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            # update the requested result with new data
            setattr(result, k, v)
    # save the updated result
    result.save()

    return jsonify(result.to_dict()), 200
