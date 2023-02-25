from flask import render_template, redirect, url_for

from . import i_userobj
from fundsapp.models import db



@i_userobj.route("/")
def home():
    return render_template("index.html")