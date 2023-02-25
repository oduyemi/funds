from flask import render_template,redirect
from . import adminobj





@adminobj.route("/")
def home():
    return "Admin Home page"