# /api

from flask import Flask, request, jsonify
from flask_cors import CORS
from redis import Redis
from api.config.default import Config
from api.routes import *
import requests

config = Config()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(routes)
    CORS(app, resources={r"/*": {"origins": "*"}})

    return app
