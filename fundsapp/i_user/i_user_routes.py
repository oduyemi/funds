import os, random, string
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField,TextAreaField, SelectField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.models import db, Industry, investment_option,I_user


from . import i_userobj








#  --  VALIDATION CLASSES  --  THESE ARE THE CLASSES FOR USER VALIDATION
class InvestSignupForm(FlaskForm):
    fname = StringField("fname",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid name"),
            Regexp(
                "^[A-Za-z] [A-Za-a0-9.]*", 0, "Your First name must contain only letters"
                ),
            ],
        render_kw={"placeholder": "Enter your first name here"})

    lname = StringField("lname",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid name"),
            Regexp(
                "^[A-Za-z] [A-Za-a0-9.]*", 0, "Your Last name must contain only letters")],
        render_kw={"placeholder": "Enter your last name here"})

    email = StringField("email",
        validators=
            [DataRequired(),
            Email()],
            render_kw={"placeholder": "Enter your email address"})
    
    password = PasswordField("password",
        validators=
            [DataRequired(),
            length(min=8, max=20)],
            render_kw={"placeholder": "Enter your password"})
    
    confirm_password = PasswordField("confirm_password",
        validators=
            [DataRequired(),
            length(min=8, max=20)],
            render_kw={"placeholder": "Confirm your password"})
    EqualTo("password", message = "The passwords must match! ")
    submit = SubmitField("Sign Up")
    
    def validate_email(self, email):
        b_user =I_user.query.filter_by(i_user_email = email.data).first()
        if i_user:
            raise ValidationError("That email already have an account. Please choose a different one.")



class InvestLoginForm(FlaskForm):
    email = StringField("email",
        validators=
            [DataRequired(),
            Email(),
            length(min=6, max=30)],
            render_kw={"placeholder": "Enter your email address"})
    
    password = PasswordField("password",
        validators=
            [DataRequired(),
            length(min=8, max=20)],
            render_kw={"placeholder": "Enter your password"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")









#         --  INVESTORS: SESSION[I_USER] --  THESE ARE THE INVESTOR ROUTES
@i_userobj.route("/", methods = (["GET", "POST"]), strict_slashes = False)
def invest_home():
    dp = db.session.query(I_user).filter(I_user.i_user_pic).first()
    fname = db.session.query(I_user).filter(I_user.i_user_fname).first()
    lname = db.session.query(I_user).filter(I_user.i_user_lname).first()
    email = db.session.query(I_user).filter(I_user.i_user_email).first()
    return render_template("investhome.html", dp = dp, fname =fname, lname = lname, email=email, title = "Homepage - Funds Investment")



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
        return redirect(url_for('iuser.login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('iuser.signup'))


@i_userobj.route('/login', methods = (["GET", "POST"]), strict_slashes = False)
def invest_login():
    session.permanent = True
    form = InvestLoginForm()
    if request.method=='GET':
        return render_template('investlogin.html', title="Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            hashed = generate_password_hash(password)
            if email !="" and password !="":
                investor = db.session.query(I_user).filter(I_user.i_user_email==email).first() 
                if investor !=None:
                    pwd =investor.i_user_password
                    chk = check_password_hash(pwd, password)
                    if chk:
                        userid = investor.i_user_id
                        session['i_user'] = userid
                        db.session.add(investor)
                        db.session.commit() 
                        return redirect(url_for('iuser.investmentdashboard'))
                    else:
                        flash('Invalid password')
                        return redirect(url_for('iuser.login'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("iuser.signup"))



@i_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
def invest_signout():
    #logout_user()
    if session.get("i_user") == None:
        session.pop("i_user", None)
    return redirect(url_for("iuser.login"))  










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
        fname = db.session.query(I_user).filter(I_user.i_user_fname).first()
        lname = db.session.query(I_user).filter(I_user.i_user_lname).first()
        email = db.session.query(I_user).filter(I_user.i_user_email).first()
        query = (f"SELECT * FROM state ORDER BY state_id")
        result = db.session.execute(text(query))
        state = result.fetchall()
        return render_template("investdashboard.html", fname =fname, lname = lname, email=email, state = state,  title = "Dashboard - Funds Investment App")
    else:
        return redirect(url_for("iuser.investlogin"))
