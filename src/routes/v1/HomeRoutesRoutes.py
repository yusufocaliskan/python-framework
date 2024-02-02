
from flask import Blueprint


home_routes = Blueprint(
    'home_routes', __name__, url_prefix='/')


@home_routes.route('/', methods=['GET'])
def home():
    return 'Welcome Test'
