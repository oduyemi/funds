from flask import Blueprint


apiobj = Blueprint("bfapi", __name__, url_prefix="/api/v1.0")


from . import api_routes