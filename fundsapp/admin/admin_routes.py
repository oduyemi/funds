from flask import render_template,redirect,request
from . import adminobj





@adminobj.route("/")
def home():
    return "Admin Home page"



@adminobj.route("/login")
def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")


@adminobj.route("/dashbboard")
def admindashboard():
    return render_template("admindashboard.html")