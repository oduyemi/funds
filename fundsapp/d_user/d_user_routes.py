import os, random, string
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField,TextAreaField, SelectField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.models import db, Industry, investment_option,D_user,Business,State
from fundsapp.forms import DonorLoginForm, DonorSignupForm


from . import d_userobj







#         --  DONORS: SESSION[D_USER] --  THESE ARE THE INVESTOR ROUTES
@d_userobj.route("/", methods = (["GET", "POST"]), strict_slashes = False)
def donatehome():
    fname = db.session.query(D_user).filter(D_user.d_user_fname).first()
    lname = db.session.query(D_user).filter(D_user.d_user_lname).first()
    email = db.session.query(D_user).filter(D_user.d_user_email).first()
    return render_template("donorhome.html", fname =fname, lname = lname, email=email, title = "Homepage - Funds Donation")



@d_userobj.route('/signup', methods = ["GET", "POST"], strict_slashes = False)
def donatesignup():
    form = DonorSignupForm()
    if request.method == "GET":
        return render_template('donorsignup.html', title="Sign Up", form = form)
    else:
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password=form.password.data
        hashedpwd = generate_password_hash(password)
    if fname !='' and lname != "" and email !='' and password !='':
        new_donor=D_user(d_user_fname = fname, d_user_lname = lname, d_user_email = email,
        d_user_password = hashedpwd)
        db.session.add(new_donor)
        db.session.commit()
        userid=new_donor.d_user_id
        session['d_user']=userid
        flash(f"Account created for {form.fname.data}! Please proceed to LOGIN ", "success")
        return redirect(url_for('duser.donatelogin'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('duser.donatesignup'))


@d_userobj.route('/login', methods = (["GET", "POST"]), strict_slashes = False)
def donatelogin():
    form = DonorLoginForm()
    if request.method=='GET':
        return render_template('donorlogin.html', title="Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            hashed = generate_password_hash(password)
            if email !="" and password !="":
                donor = db.session.query(D_user).filter(D_user.d_user_email==email).first() 
                if donor !=None:
                    pwd =donor.d_user_password
                    chk = check_password_hash(pwd, password)
                    if chk:
                        userid = donor.d_user_id
                        session['d_user'] = userid
                        db.session.add(donor)
                        db.session.commit() 
                        return redirect(url_for('duser.donationdashboard'))
                    else:
                        flash('Invalid password')
                        return redirect(url_for('duser.donatelogin'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("duser.donatesignup"))



@d_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
def donatesignout():
    if session.get("d_user") == None:
        session.pop("d_user", None)
    return redirect(url_for("duser.donatelogin"))  










#         --  DASHBOARDS  --  THESE ARE THE INVESTMENT DASHBOARD ROUTES
@d_userobj.route('/dashboardlayout', methods = ("GET", "POST"), strict_slashes = False)
def donor_dashboardlayout():
    fname = db.session.query(D_user).filter(D_user.d_user_fname).first()
    lname = db.session.query(D_user).filter(D_user.d_user_lname).first()
    email = db.session.query(D_user).filter(D_user.d_user_email).first()
    return render_template("donordashboardlayout.html", fname = fname, lname = lname, email = email,  title = "Dashboard - Funds Investment App")
    


@d_userobj.route('/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def donationdashboard():
    if session.get("d_user") != None:
        user = db.session.query(D_user).first()
        industry = db.session.query(Industry).order_by(Industry.industry_id).all()
        reg1 = db.session.query(Business).filter(Business.business_type==2).all()
        reg2 = db.session.query(Business).filter(Business.business_type==3).all()
        pend1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        pend2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        app2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        #fund = db.session.query(Business_disbursement).filter(Business_disbursement.business_id).all()
        query = f"SELECT * from business WHERE (business_type=2 or business_type=3) and business_status_id=2"
        content = db.session.execute(text(query))
        registered = int(len(reg1) + int(len(reg2)))
        pending = int(len(pend1)) + int(len(pend2))
        approved = int(len(app1)) + int(len(app2))
        #funded = len(fund)
        return render_template("donordashboard.html", registered=registered, pending=pending, approved=approved,
        user=user, industry = industry, content=content, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("duser.donatelogin"))


@d_userobj.route('/pitch/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def donatepitch():
    id=session.get("d_user")
    if id != None:
        user = db.session.query(D_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg1 = db.session.query(Business).filter(Business.business_type==2).all()
        reg2 = db.session.query(Business).filter(Business.business_type==3).all()
        pend1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        pend2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        app2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE (business_type=2 or business_type=3) and business_status_id=2"
        content = db.session.execute(text(query))
        #fund = db.session.query(Business_disbursement).join(Business, Business.business_disbursement_id).order_by(Business_disbursement.business_id).where(Business.Business_type==2).all()
        registered = int(len(reg1) + int(len(reg2)))
        pending = int(len(pend1)) + int(len(pend2))
        approved = int(len(app1)) + int(len(app2))
        #funded = len(fund)
        return render_template("donorpitch.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("duser.donatelogin"))


@d_userobj.route('/list/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def donatelist():
    id=session.get("d_user")
    if id != None:
        state = db.session.query(State).order_by(State.state_id).all()
        user = db.session.query(D_user).first()
        reg1 = db.session.query(Business).filter(Business.business_type==2).all()
        reg2 = db.session.query(Business).filter(Business.business_type==3).all()
        pend1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        pend2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        app2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE (business_type=2 or business_type=3) and (business_status_id=1 or business_status_id=2)" 
        content = db.session.execute(text(query))
        #fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = int(len(reg1) + int(len(reg2)))
        pending = int(len(pend1)) + int(len(pend2))
        approved = int(len(app1)) + int(len(app2))
        #funded = len(fund)
        return render_template("donorlist.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("duser.donatelogin"))

@d_userobj.route('/account/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def donateaccount():
    id=session.get("d_user")
    if id != None:
        user = db.session.query(D_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).filter(Business.business_type==1).all()
        pend = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
        query = f"SELECT business_name, industry_name, business_desc, business_email from business JOIN industry ON business_id WHERE business_type=1 AND business_status_id=2 AND industry_id=business_industryid ORDER BY business_id"
        content = db.session.execute(text(query))
        #fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==1).all()
        registered = int(len(reg))
        pending = int(len(pend))
        approved = int(len(app)) 
        #funded = len(fund)
        return render_template("donoraccount.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("duser.donatelogin"))


@d_userobj.route('/donation/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def donateinvestment():
    id=session.get("d_user")
    user = db.session.query(D_user).first()
    reg1 = db.session.query(Business).filter(Business.business_type==2).all()
    reg2 = db.session.query(Business).filter(Business.business_type==3).all()
    pend1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
    pend2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
    app1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
    app2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
    registered = int(len(reg1) + int(len(reg2)))
    pending = int(len(pend1)) + int(len(pend2))
    approved = int(len(app1)) + int(len(app2))
    if id != None:
        return render_template("donorinvest.html", registered=registered, pending=pending, approved=approved,
        user=user, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("duser.donatelogin"))

