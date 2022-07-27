from flask import current_app, jsonify, request
from api.utils.auth import auth_required
from api.db.redis import get_redis
from . import coingecko
import requests
import json

# TODO: Implement caching on these routes
@coingecko.route(f'/simple/price/', methods=['GET'], strict_slashes=False)
@auth_required
def simple_price():
    base_url = current_app.config['THIRD_PARTY_API_URL']
    args = request.args
    ids_query = args.get('ids')
    vs_currencies_query = args.get('vs_currencies')

    # Require param ids
    if not ids_query:
        return jsonify({
            "error": "Missing parameter ids"
        }), 422

    # Require param vs_currencies
    if not vs_currencies_query:
        return jsonify({
            "error": "Missing parameter vs_currencies"
        }), 422

    # Submit request to CoinGecko
    url = f"{base_url}/simple/price?ids={ids_query}&vs_currencies={vs_currencies_query}"

    response = requests.get(url)
    response_json = response.json()
       
    return jsonify(response_json), 200
