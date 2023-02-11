from flask import render_template, redirect, flash, session, request, url_for
from sqlalchemy.sql import text

from werkzeug.security import generate_password_hash, check_password_hash

from fundsapp import starter, db

from fundsapp.models import Investor

@starter.route('/invest')
def invest_home():
    return render_template("invest/home.html")
    
@starter.route('invest/login', methods=["POST","GET"])
def invest_login():
    if request.method == "GET":
        return render_template("invest/login.html")
    else:
        email = request.form.get('email')
        password = request.form.get('pwd')
        query = f"SELECT * FROM investor WHERE investor_email='{email}'"
        result = db.session.execute(text(query))
        total = result.fetchone()
        if total:
            pwd_indb = total[2]
            chk = check_password_hash(pwd_indb, password)
            if chk:
                session['investloggedin'] = email
                return redirect('/invest/dashboard')
            else:
                flash("<div class='alert alert-danger'>Invalid credentials</div>")
                return redirect('/invest/login')
        else:
            flash("<div class='alert alert-danger'>Invalid credentials</div>")
            return redirect('/invest/login')

@starter.route("/invest/signup")
def invest_signup():
    return render_template("invest/signup.html")


@starter.route('/invest/dashboard')
def invest_dashboard():
    if session.get('investloggedin') != None:
        id = session['investloggedin']
        deets = db.session.query(Investor).get(id)
        email = deets.investor_email
        return render_template('invest/dashboard.html', deets = deets, email = email)
        
    else:
        return redirect('/invest/login')
    