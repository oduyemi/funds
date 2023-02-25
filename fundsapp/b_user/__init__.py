from flask import Blueprint
b_userobj = Blueprint("fbuser", __name__, template_folder="templates", static_folder="static")



from . import b_user_routes




