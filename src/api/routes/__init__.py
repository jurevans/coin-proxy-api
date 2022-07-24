# /api/routes

from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .rates import *
from .health import *
from .env import *
