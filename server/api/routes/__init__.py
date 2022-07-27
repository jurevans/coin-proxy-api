# /api/routes

from flask import Blueprint

API_PREFIX = '/api/v1'
routes = Blueprint('routes', __name__, url_prefix=API_PREFIX)

from .coingecko import coingecko
routes.register_blueprint(coingecko)

from .index import *
from .rates import *
from .health import *
from .env import *
