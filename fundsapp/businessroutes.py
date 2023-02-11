from flask import render_template, request, redirect, flash, session, request, url_for
from sqlalchemy.sql import text

from werkzeug.security import generate_password_hash, check_password_hash 

from fundsapp import starter, db

from fundsapp.models import Business_owner

@starter.route('/')
def indexpage():
    return render_template('business/index.html')

@starter.route('/dashboard')
def business_dashboard():
    if session.get('businessloggedin') != None:
        id = session['businessloggedin']
        deets = db.session.query(Business_owner).get(id)
        email = deets.entrepreneur_email
        return render_template('business/dashboard.html',deets = deets, email = email)
        
    else:
        return redirect('/login')
    

@starter.route('/login', methods=["POST","GET"])
def business_login():
    if request.method == "GET":
        return render_template("business/login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('pwd')
        #write your select query
        query = f"SELECT * FROM entrepreneur WHERE entrepreneur_email='{email}'"
        result = db.session.execute(text(query))
        total = result.fetchone()
        if total:
            pwd_indb = total[2]
            chk = check_password_hash(pwd_indb, password)
            if chk:
                session['businessloggedin'] = email
                return redirect('/dashboard')
            else:
                flash("<div class='alert alert-danger'>Invalid credentials</div>")
                return redirect('/login')
        else:
            flash("<div class='alert alert-danger'>Invalid credentials</div>")
            return redirect('/login')

@starter.route('/signup')
def business_signup():
    return render_template('business/signup.html')

@starter.route("/home")
def business_home():
    return render_template("business/home.html")

@starter.route('/ngo')
def ngopage():
    return render_template('business/ngo.html')

@starter.route('/prestartup')
def prestartpage():
    return render_template('business/prestartup.html')

@starter.route('/startup')
def startuppage():
    return render_template('business/startup.html')

@starter.route('/donate')
def donatepage():
    return render_template('business/donate.html')


@starter.route('/layout1')
def layout1page():
    return render_template('business/layout1.html')