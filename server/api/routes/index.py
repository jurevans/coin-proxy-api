from flask import jsonify
from api.utils.auth import auth_required
from . import routes

@routes.route('/', methods=['GET'], strict_slashes=False)
@auth_required
def index():
    return jsonify({
        'version': '1.0.1'
    }), 200
