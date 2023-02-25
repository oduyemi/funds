from flask import Blueprint


adminobj = Blueprint("bpadmin", __name__, template_folder="templates", static_folder="static", url_prefix = "/admin")


from . import admin_routes