from flask import current_app, jsonify, request
from api.utils.auth import auth_required
from api.utils.helpers import (comma_separated_params_to_list, get_timestamp,
                              make_storage_key, fetch_exchange_rate)
from api.db.redis import get_redis
from . import routes

@routes.route('/rates', methods=['GET', 'POST'], strict_slashes=False)
@auth_required
def rates():
    redis_client = get_redis()
    config = current_app.config
    tokens = []
    fiat_currencies = []
    exchange_rates = {}

    if request.is_json:
        content = request.get_json()

        tokens = content['coins'] if 'coins' in content else []
        fiat_currencies = content['currencies'] if 'currencies' in content else []
    else:
        args = request.args
        coins = args.get('coin') or args.get('coins')
        currencies = args.get('currency') or args.get('currencies')

        if coins:
            tokens = comma_separated_params_to_list(coins)

        if currencies:
            fiat_currencies = comma_separated_params_to_list(currencies)

    tokens = tokens if tokens else config['DEFAULT_TOKENS']
    fiat_currencies = fiat_currencies if fiat_currencies else config['DEFAULT_CURRENCIES']

    for token in tokens:
        exchange_rates[token] = {}
        for fiat in fiat_currencies:
            key = make_storage_key(token, fiat)
            expires_key = f"{key}/expires"
            unexpired = redis_client.get(expires_key)
            data = redis_client.hgetall(key)

            if not unexpired:
                data = fetch_exchange_rate(token, fiat)
                if bool(data):
                    redis_client.set(expires_key, config['TTL'], ex=config['TTL'])
                    redis_client.hset(name=make_storage_key(token, fiat), mapping=data)
                else:
                    data = {}

            # Provide conversion rate in float
            if bool(data):
                rate = data['rate']
                data['rate'] = float(rate) if rate else 0

            exchange_rates[token][fiat] = data

    return jsonify({
        'data': exchange_rates,
        'timestamp': get_timestamp(),
    })
