from flask import Blueprint


i_userobj = Blueprint("iuser", __name__, template_folder="templates", static_folder="static", url_prefix = "/invest")


from . import i_user_routes