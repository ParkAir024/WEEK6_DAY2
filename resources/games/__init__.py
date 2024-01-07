from flask_smorest import Blueprint

bp = Blueprint('games', __name__, description='Ops on Games', url_prefix='/games')

from . import routes