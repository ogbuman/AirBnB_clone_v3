#!/usr/bin/python3
""" places_amenities api v1 view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """ return amenities """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities), 200

# delete amenity from place


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ Deletes a amenity object

    Args:
        amenity_id (str):amenity id to delete
    """
    place = storage.get("Place", str(place_id))
    if not place:
        abort(404)
    amenity = storage.get("Amenity", str(amenity_id))
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    # remove amenity from place
    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


# link amenity to place
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """ Link a amenity object

    Args:
        amenity_id (str):amenity id to link
    """
    place = storage.get("Place", str(place_id))
    if not place:
        abort(404)
    amenity = storage.get("Amenity", str(amenity_id))
    if not amenity:
        abort(404)
    # if amenity already linked to place
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    # add amenity to place
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
