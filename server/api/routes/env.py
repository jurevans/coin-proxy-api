from flask import jsonify
from healthcheck import EnvironmentDump
from api.utils.auth import auth_required
from . import routes

envdump = EnvironmentDump()

def application_data():
    return {'maintainer': 'Justin R. Evans',
            'git_repo': 'https://github.com/jurevans/coin-cache-api'}

envdump.add_section('application', application_data)

@routes.route('/env', methods=['GET'], strict_slashes=False)
@auth_required
def env():
    return envdump.run()
