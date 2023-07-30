#!/usr/bin/python3
""" places_reviews api v1 view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ return reviews """
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200

# get a review by id


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """ return review by id """
    review = storage.get("Review", str(review_id))
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200

# delete a review by id


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review object

    Args:
        review_id (str):review id to delete
    """
    review = storage.get("Review", str(review_id))
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a review object

    Args:
        place_id (str): place id to create review for
    """
    place = storage.get("Place", str(place_id))
    if not place:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    if "user_id" not in params_json:
        abort(400, "Missing user_id")
    if "text" not in params_json:
        abort(400, "Missing text")
    user = storage.get("User", params_json["user_id"])
    if not user:
        abort(404)
    review = request.get_json()
    review["place_id"] = place_id
    review = Review(**review)
    review.save()
    return jsonify(review.to_dict()), 201

# update a review by id


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a review object

    Args:
        review_id (str): review id to update
    """
    review = storage.get("Review", str(review_id))
    if not review:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    for key, value in params_json.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
