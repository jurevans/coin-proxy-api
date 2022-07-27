# /api/routes/coingecko

from flask import Blueprint
coingecko = Blueprint('coingecko', __name__, url_prefix='/coingecko')

'''
Routes under /coingecko support the native API
'''

from .simple_price import *
from .coins_list import *
