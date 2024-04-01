#!/usr/bin/python3
"""
app
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    close db
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error
    """
    err = {
        "error": "Not found"
    }

    res = jsonify(err)
    res.status_code = 404

    return res

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
