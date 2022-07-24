from flask import jsonify
from healthcheck import HealthCheck
from api.db.redis import redis_available
from api.utils.auth import auth_required
from . import routes

@routes.route('/health', methods=['GET'], strict_slashes=False)
@auth_required
def health():
    health = HealthCheck()
    health.add_check(redis_available)
    return health.run()
