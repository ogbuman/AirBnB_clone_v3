#!/usr/bin/python3
""" amenities api view
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


# get all
@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """ get all amenities
    """

    amenities_list = []
    # get all amenities
    amenities = storage.all(Amenity)

    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list), 200


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenities_id(amenity_id):
    """ get amenity by id

    Args:
        amenity_id (str): amenity id
    """

    # get an amenity by id
    amenity = storage.get("Amenity", str(amenity_id))

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """ delete an amenity

    Args:
        amenity_id (str): amenity id
    """

    amenity = storage.get("Amenity", str(amenity_id))

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenities():
    """ create a amenity
    """
    # get params
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")

    if "name" not in params_json:
        abort(400, "Missing name")

    # create new amenity instance

    new_amenity = Amenity(**params_json)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """ update an amenity

    Args:
        amenity_id (str): amenity id
    """
    # get the amenity dict to be updated
    amenity = storage.get("Amenity", str(amenity_id))

    # if amenity with the id does not exist abort with 404
    if not amenity:
        abort(404)

    # get params to update
    params_json = request.get_json()

    if not params_json:
        abort(400, "Not a JSON")

    for k, v in params_json.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
