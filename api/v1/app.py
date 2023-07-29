#!/usr/bin/python3
""" Flask app api """

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
# enable cors for all domains on all routes
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# register blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle the 404 error and gives the json formatted response"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True)
