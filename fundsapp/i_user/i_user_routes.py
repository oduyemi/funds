import os, random, string
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField,TextAreaField, SelectField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.models import db, Industry, investment_option, I_user, Business_disbursement, Business, Industry,B_user,State
from fundsapp.forms import InvestLoginForm, InvestSignupForm

from . import i_userobj


#         --  INVESTORS: SESSION[I_USER] --  THESE ARE THE INVESTOR ROUTES
@i_userobj.route("/", methods = (["GET", "POST"]), strict_slashes = False)
def invest_home():
    fname = db.session.query(I_user).filter(I_user.i_user_fname).first()
    lname = db.session.query(I_user).filter(I_user.i_user_lname).first()
    email = db.session.query(I_user).filter(I_user.i_user_email).first()
    return render_template("investhome.html", fname =fname, lname = lname, email=email, title = "Homepage - Funds Investment")



@i_userobj.route('/signup', methods = ["GET", "POST"], strict_slashes = False)
def invest_signup():
    form = InvestSignupForm()
    if request.method == "GET":
        return render_template('investsignup.html', title="Sign Up", form = form)
    else:
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password=form.password.data
        hashedpwd = generate_password_hash(password)
    if fname !='' and lname != "" and email !='' and password !='':
        new_investor=I_user(i_user_fname = fname, i_user_lname = lname, i_user_email = email,
        i_user_password = hashedpwd)
        db.session.add(new_investor)
        db.session.commit()
        userid=new_investor.i_user_id
        session['i_user']=userid
        flash(f"Account created for {form.fname.data}! Please proceed to LOGIN ", "success")
        return redirect(url_for('iuser.invest_login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        #return redirect(url_for('iuser.invest_signup'))


@i_userobj.route('/login', methods = (["GET", "POST"]), strict_slashes = False)
def invest_login():
    form = InvestLoginForm()
    if request.method=='GET':
        return render_template('investlogin.html', title="Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            #hashed = generate_password_hash(password)
            if email !="" and password !="":
                user = db.session.query(I_user).filter(I_user.i_user_email==email).first() 
                if user !=None:
                    pwd =user.i_user_password
                    chk = check_password_hash(pwd, password)
                    if chk:
                        userid = user.i_user_id
                        session['i_user'] = userid
                        return redirect(url_for('iuser.investmentdashboard'))
                    else:
                        flash('Invalid email or password', "danger")
                        return redirect(url_for('iuser.invest_login'))
            else:
                flash("Verify that all fields are correctly filled", "danger")
                return redirect(url_for("iuser.invest_login"))
                



@i_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
def invest_signout():
    #logout_user()
    if session.get("i_user") != None:
        session.pop("i_user", None)
    return redirect(url_for("iuser.invest_login"))  










#         --  DASHBOARDS  --  THESE ARE THE INVESTMENT DASHBOARD ROUTES
@i_userobj.route('/dashboardlayout', methods = ("GET", "POST"), strict_slashes = False)
def invest_dashboardlayout():
    fname = db.session.query(I_user).filter(I_user.i_user_fname).first()
    lname = db.session.query(I_user).filter(I_user.i_user_lname).first()
    email = db.session.query(I_user).filter(I_user.i_user_email).first()
    return render_template("investdashboardlayout.html", fname = fname, lname = lname, email = email,  title = "Dashboard - Funds Investment App")
    


@i_userobj.route('/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def investmentdashboard():
    if session.get("i_user") != None:
        user = db.session.query(I_user).first()
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
        return render_template("investdashboard.html", registered=registered, pending=pending, approved=approved,
        user=user, industry = industry, content=content, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("iuser.invest_login"))


@i_userobj.route('/pitch/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def investpitch():
    id=session.get("i_user")
    if id != None:
        user = db.session.query(I_user).first()
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
        return render_template("investpitch.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("iuser.invest_login"))


@i_userobj.route('/list/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def investlist():
    id=session.get("i_user")
    if id != None:
        state = db.session.query(State).order_by(State.state_id).all()
        user = db.session.query(I_user).first()
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
        return render_template("investlist.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("iuser.invest_login"))

@i_userobj.route('/account/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def investaccount():
    id=session.get("i_user")
    if id != None:
        user = db.session.query(I_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg1 = db.session.query(Business).filter(Business.business_type==2).all()
        reg2 = db.session.query(Business).filter(Business.business_type==3).all()
        pend1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        pend2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app1 = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        app2 = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT business_name, industry_name, business_desc, business_email from business JOIN industry ON business_id WHERE (business_type=2 or business_type=3) AND business_status_id=2 AND industry_id=business_industryid ORDER BY business_id"
        content = db.session.execute(text(query))
        #fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = int(len(reg1) + int(len(reg2)))
        pending = int(len(pend1)) + int(len(pend2))
        approved = int(len(app1)) + int(len(app2))
        #funded = len(fund)
        return render_template("investaccount.html", registered=registered, pending=pending, approved=approved,
        user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("iuser.invest_login"))


@i_userobj.route('/investment/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def invest_investment():
    id=session.get("i_user")
    user = db.session.query(I_user).first()
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
        return render_template("investinvest.html", registered=registered, pending=pending, approved=approved,
        user=user, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("iuser.invest_login"))

@i_userobj.route("/howitworks",strict_slashes=False)
def b_how():
    user = db.session.query(I_user).first()
           
    return render_template("howitworks.html",user=user)


