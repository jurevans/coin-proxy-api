from flask import request, jsonify
from flask_httpauth import HTTPTokenAuth
from functools import wraps
from api.config import Config

config = Config()
auth = HTTPTokenAuth(header={ 'X-API-Key': config.API_KEY } )

@auth.verify_token
def verify_token(token=None):
    headers = request.headers
    key = headers.get('X-Api-Key')
    return key == config.API_KEY

@auth.error_handler
def auth_error(status):
    return jsonify({
        'message': 'Access Denied',
        'status': status
    }), 401

def auth_required(f):
    @auth.login_required
    @wraps(f)
    def wrap(*args, **kwargs):
        return f(*args, **kwargs)
    return wrap
