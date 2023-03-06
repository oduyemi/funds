from flask import Blueprint


d_userobj = Blueprint("duser", __name__, template_folder="templates", static_folder="static", url_prefix = "/donation")


from . import d_user_routes