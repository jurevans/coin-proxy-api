# coin-cache-api

This is a simple Rest API for caching fiat-conversion rates from a third-party API, and may potentially serve other useful data in the future. This API is built on Python, Flask, and Redis. Data from a third-party API are stored as a hashmap in Redis with a designated TTL. The client can either use the timestamp of the original third-party request for each token and currency, or the timestamp of the request to this API to determine a sane time to refetch results. Each token and currency combination is requested and cached individually.

## Table of Contents

- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the development server](#running-the-development-server)
- [Using with docker-compose](#using-with-docker-compose)
- [Endpoints](#endpoints)
- [Notes](#notes)
- [TODO](#todo)

## Installation

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
. venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

[ [Table of Contents](#table-of-contents) ]

## Environment Configuration

Create a `.env` file (in the base project directory) with the following keys defined:

```bash
# Key used by x-api-key header to authorize protected routes - REQUIRED
API_KEY="THIS_IS_MY_API_KEY"

# Redis authentication - REQUIRED (if your Redis host requires AUTH)
REDIS_PASSWORD="MY_REDIS_SECRET"

# Redis host (if not localhost) - OPTIONAL
REDIS_HOST="domain.of.redishost"

# Redis port (if not default) - OPTIONAL
REDIS_PORT=6379

# Redis db, defaults to 0 - OPTIONAL
REDIS_DB=0

# API KEY for rest.coinapi.io - REQUIRED
THIRD_PARTY_KEY="xxxxxx-xxxx-xxxxxx-xxxxxxxxx-xxxxxxxx"

# Exchange Rate API URL - OPTIONAL
EXCHANGE_RATE_API="https://rest.coinapi.io/v1/exchangerate"

# TTL for cached API queries (third-party), defaults to 7200 (2 hours) - OPTIONAL
TTL = 3600
```

Additionally, see `DEFAULTS` in `api/config/default.py` for setting default tokens, currencies, etc.

[ [Table of Contents](#table-of-contents) ]

## Running the development server

```bash
export FLASK_APP=src/api

flask run
# Your server will be available at http://127.0.0.1:5000/
# Make sure to send requests with the x-api-key header value which
# matches the key in your .env file
```

[ [Table of Contents](#table-of-contents) ]

## Using with docker-compose

In the project directory (`coin-cache-api`), run the following:

```bash
docker-compose build
docker-compose up -d
```

Check that the containers are up and running:

```bash
docker-compose ps
```

[ [Table of Contents](#table-of-contents) ]

## Endpoints

- `/api/v1` - Version info
- `/api/v1/rates` - Get default conversion rates (`GET`|`POST`)
- `/api/v1/rates?coins=BTC,ETH,DOT` - Specify coins for which to query. Default currencies will be used.
- `/api/v1/rates?currencies=USD,EUR` - Specify currencies. Default coins will be used.
- `/api/v1/rates?coins=BTC,ETH,DOT,ATOM&currencies=USD,YEN,EUR` - Specify both coins and currencies, no defaults.
- `/api/v1/health` - Health check
- `/api/v1/env` - Environment variables

**POST** Example with cURL

_NOTE_ You can specify `coin` or `coins`, `currency` or `currencies` as the `GET` request parameters with similar effect.

_NOTE_ `POST` requests can also be sent as JSON data, passing `coins` and/or `currencies` as JSON parameters. Passing no arguments in a `POST` or `GET` will return the API default values.

```bash
curl --request POST http://127.0.0.1:5000/api/v1/rates --header "X-Api-Key:MY_SECRET_API_KEY" --data "coins=BTC,EUR&currencies=USD,EUR,YEN"

# Optionally, pipe it through jq for formatting JSON
curl --request POST http://127.0.0.1:5000/api/v1/rates --header "X-Api-Key:MY_SECRET_API_KEY" --data "coins=BTC,EUR&currencies=USD,EUR,YEN" | jq
```

**SAMPLE OUTPUT**

```json
{
  "data": {
    "BTC": {
      "EUR": {
        "coin": "BTC",
        "currency": "EUR",
        "rate": 23268.18602491288,
        "timestamp": "2022-07-20T13:05:06.0000000Z"
      },
      "USD": {
        "coin": "BTC",
        "currency": "USD",
        "rate": 23838.256582523245,
        "timestamp": "2022-07-20T13:05:06.0000000Z"
      },
      "YEN": {}
    },
    "EUR": {
      "EUR": {
        "coin": "EUR",
        "currency": "EUR",
        "rate": 1.0,
        "timestamp": "2022-07-20T13:18:07.6269666Z"
      },
      "USD": {
        "coin": "EUR",
        "currency": "USD",
        "rate": 1.0245,
        "timestamp": "2022-07-20T13:17:57.0000000Z"
      },
      "YEN": {}
    }
  },
  "timestamp": 1658323087.77571
}
```

_NOTE_ In this example, no conversion rates were found for `YEN` (the correct currency value would be `JPY`), which results in an empty JSON object. Empty results are not cached, and will be refetched on the next request.

[ [Table of Contents](#table-of-contents) ]

## Notes

Using `redis-cli`, we can inspect the cached values from our third-party requests.

```bash
redis-cli
```

If authentication is required, enter the proper password (as defined in `.env`):

```bash
AUTH <my-secret-redis-password>
```

Inspecting the stored keys following a request, you may see something like the following:

```bash
127.0.0.1:6379> keys *
 1) "DOT/USD/expires"
 2) "DOT/USD"
 3) "BTC/USD/expires"
 4) "BTC/USD"
...
```

As the API results are cached as hashmaps (which, in Redis, do not accept a TTL), an `/expires` key/value is set, expiring when the configured TTL has been reached. These keys are checked to determine when a refetch should occur, which will overwrite the cached hashmaps. We can inspect one of these hashmaps as such:

```bash
127.0.0.1:6379> hgetall "BTC/USD"
```

The value for the `/expires` key, e.g., `BTC/USD/expires`, is set to TTL it was given:

```bash
127.0.0.1:6379> get "BTC/USD/expires"
"7200"
```

[ [Table of Contents](#table-of-contents) ]

## TODO

- Use the same format and type for timestamps.
- Any error responses from the third-party API should be passed on to the client for handling.
- Implement caching on all routes, not just `/api/v1/rates`, where applicable

[ [Table of Contents](#table-of-contents) ]
