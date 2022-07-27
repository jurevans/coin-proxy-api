from flask import current_app, jsonify, request
from api.utils.auth import auth_required
from . import coingecko
import requests
import json

# TODO: Implement caching on this route
@coingecko.route(f'/coins/list/', methods=['GET'], strict_slashes=False)
@auth_required
def coins_list():
    base_url = current_app.config['THIRD_PARTY_API_URL']

    # Submit request to CoinGecko
    url = f"{base_url}/coins/list"

    response = requests.get(url)
    response_json = response.json()

    return jsonify(response_json), 200
