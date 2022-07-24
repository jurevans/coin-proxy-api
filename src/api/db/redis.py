from flask import g
from api.config import Config
from redis import Redis

def get_redis():
    if 'db' not in g:
        config = Config()
        g.db = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT,
                     password=config.REDIS_PASSWORD, db=config.REDIS_DB, decode_responses=True)
    return g.db

def redis_available():
    redis_client = get_redis()
    info = redis_client.info()
    return True, 'redis ok'
