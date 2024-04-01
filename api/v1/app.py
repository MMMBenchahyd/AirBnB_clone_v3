#!/usr/bin/python3
"""
app API
"""

from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    close db
    """
    storage.close()


@app.errorhandler(404)
def handle_er(exception):
    """
    return 404 not fount
    """
    err = {"error": "Not found"}
    return jsonify(err), 404


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv(
        "HBNB_API_PORT"), threaded=True, debug=True)
