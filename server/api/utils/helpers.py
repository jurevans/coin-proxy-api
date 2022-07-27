from api.config.default import Config
from datetime import datetime
import requests

config = Config()

def comma_separated_params_to_list(param):
    result = []
    for val in param.split(','):
        if val:
            result.append(val.strip())
    return result

def get_timestamp():
    return datetime.timestamp(datetime.now())

def make_storage_key(token, fiat):
    return f"{token}/{fiat}"

def fetch_exchange_rate(token, fiat):
    url = f"{config.EXCHANGE_RATE_API}/{token}/{fiat}/"
    headers = {'X-CoinAPI-Key' : config.THIRD_PARTY_KEY}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    data = {}

    if response:
        data = {
            'coin': response_json['asset_id_base'] or token,
            'currency': response_json['asset_id_quote'] or fiat,
            'rate': response_json['rate'],
            'timestamp': response_json['time'],
        }

    return data
