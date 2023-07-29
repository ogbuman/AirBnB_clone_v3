#!/usr/bin/python3
""" index api v1 view """

from api.v1.views import app_views
from flask import jsonify
from models import storage

# api route for status


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return status """
    return jsonify({"status": "OK"}), 200

# api route for tables stats


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ return stats """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")}), 200
