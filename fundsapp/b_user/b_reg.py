import os, random, string, requests,json
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
# from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.forms import LoginForm, SignupForm, RegistrationForm
from fundsapp.models import B_user, db, State, Industry, Business_type, Business, Business_disbursement

from . import b_reg


def generate_name():
    global filename
    filename = random.sample(string.ascii_lowercase,10) #this will return a list
    return ''.join(filename) #here we join every member of the list "filename"




#         --  FORM AUTHENTICATION  --  THESE ARE THE USER FORM ROUTES AND AUTHENITCATION
@b_reg.route("/registration", methods = ("GET", "POST"), strict_slashes = False)
def reg2():
    if session.get("user") != None:
        reg = request.files['reg']
        filename = reg.filename 
        filetype = reg.mimetype 
        allowed = ['.png','.jpg','.jpeg', '.pdf']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                reg.save("fundsapp/static/uploads/"+newname) 
            else:
                return "File not allowed!"
        else:
            flash("Please choose a File")


        tax = request.files["tax"]
        filename = tax.filename 
        filetype = tax.mimetype 
        allowed = ['.png','.jpg','.jpeg', 'pdf']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                tax.save("fundsapp/static/uploads/"+newname) 
            else:
                return "File not allowed!"
        else:
            flash("Please choose a File")

        plan = request.files["plan"]
        filename = plan.filename 
        filetype = plan.mimetype 
        allowed = ['.doc','.docx','.pdf', '.txt']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                plan.save("fundsapp/static/uploads/"+newname) 
            else:
                return "File not allowed!"
        else:
            flash("Please choose a File")

        img1 = request.files["img1"]
        filename = img1.filename 
        filetype = img1.mimetype 
        allowed = ['.png','.jpg','.jpeg']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                img1.save("fundsapp/static/uploads/"+newname) 
            else:
                return "Images only!"
        else:
            flash("Please choose a File") 

        img2 = request.files["img2"]
        filename = img2.filename 
        filetype = img2.mimetype 
        allowed = ['.png','.jpg','.jpeg']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                img2.save("fundsapp/static/uploads/"+newname) 
            else:
                return "Images only!"
        else:
            flash("Please choose a File") 

        img3 = request.files["img3"]
        filename = img3.filename 
        filetype = img3.mimetype 
        allowed = ['.png','.jpg','.jpeg']
        if filename !="":
            name,ext = os.path.splitext(filename) 
            if ext.lower() in allowed: 
                newname = generate_name()+ext
                img3.save("fundsapp/static/uploads/"+newname) 
            else:
                return "Images only!"
        else:
            flash("Please choose a File") 
    return render_template("reg2.html")



