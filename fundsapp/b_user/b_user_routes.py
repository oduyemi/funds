import os, random,string
from flask import Flask
from flask import render_template, redirect, url_for, request, flash, session, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from fundsapp.models import B_user, db

from . import b_userobj



#         --  VALIDATION CLASSES  --  THESE ARE THE CLASSES FOR USER VALIDATION
class SignupForm(FlaskForm):
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
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")



class LoginForm(FlaskForm):
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



class RegistrationForm(FlaskForm):
    businessname = StringField("fname",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid name"),
            Regexp(
                "^[A-Za-z] [A-Za-a0-9.]*", 0, "Your Business name must contain only letters"
                ),
            ],
        render_kw={"placeholder": "Enter your business name here"})

    phone = StringField("lname",
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
    
    def validate_email(self,email):
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")






#         --  FORM AUTHENTICATION  --  THESE ARE THE USER FORM ROUTES AND AUTHENITCATION
@b_userobj.route('/signup', methods = ["GET", "POST"], strict_slashes = False)
def signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template('signup.html', title="Sign Up", form = form)
    else:
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password=form.password.data
        hashedpwd = generate_password_hash(password)
    if fname !='' and lname != "" and email !='' and password !='':
        new_user=B_user(b_user_fname = fname, b_user_lname = lname, b_user_email = email,
        b_user_password = hashedpwd)
        db.session.add(new_user)
        db.session.commit()
        userid=new_user.b_user_id
        session['user']=userid
        flash(f"Account created for {form.fname.data}! Please proceed to LOGIN ", "success")
        return redirect(url_for('fbuser.login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('fbuser.signup'))



@b_userobj.route('/login', methods = (["GET", "POST"]), strict_slashes = False)
def login():
    session.permanent = True
    form = LoginForm()
    email = form.email.data
    if request.method=='GET':
        return render_template('login.html', title="Login", form=form)
    else:
        #retrieve the form data
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        #run a query to know if the username exists on the database 
        deets = db.session.query(B_user).filter(B_user.b_user_email==email).first() 
        if deets !=None:
            pwd_indb = deets.b_user_password
            chk = check_password_hash(pwd_indb, pwd)
            if chk:
                #log in the person
                id = deets.b_user_id
                session['user'] = id
                return redirect(url_for('fbuser.dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('fbuser.login'))
        else:
            return redirect(url_for('fbuser.login'))



@b_userobj.route("/register", methods = ("GET", "POST"), strict_slashes = False)
def register():
    return render_template("register.html")



@b_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
#@login_required
def signout():
    #logout_user()
    if session.get("user") != None:
        session.pop("user",None)
    return redirect(url_for("fbuser.login"))    





#         --  USERS: SESSION[USER] --  THESE ARE THE USER ROUTES
@b_userobj.route('/', methods = (["GET", "POST"]), strict_slashes = False)
def indexpage():
    return render_template('index.html', title = "Funds App")



@b_userobj.route("/home", methods = ("GET", "POST"), strict_slashes = False)
def home():
    return render_template("home.html",  title = "Homepage - Funds App")



@b_userobj.route("/profile", methods=['POST', 'GET'], strict_slashes = False)
def profile():
    id = session.get('user')
    if id ==None:
        return redirect(url_for('fbuser.login'))
    else:
        if request.method =='GET':
            deets = db.session.query(B_user).filter(B_user.b_user_id==id).first()
            return render_template('profile.html',deets=deets)
        else:
            #form was submitted
            #To do: retrieve from data (fullname and phone), save them in respective variables 
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            email = request.form.get('email')
            #update query
            userobj = db.session.query(B_user).get(id)
            userobj.b_user_fname=fname
            userobj.b_user_lname=lname
            userobj.user_email =email
            db.session.commit()
            flash('Profile Updated')
            return redirect(url_for('fbuser.dashboard'))





#         --  DASHBOARDS  --  THESE ARE THE USER DASHBOARD ROUTES
@b_userobj.route('/ngo/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngodashboard():
    if session.get("user") != None:
        return render_template("ngo_dashboard.html",  title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.login"))



@b_userobj.route('/startup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startupdashboard():
    if session.get("user") != None:
        return render_template("startup_dashboard.html",  title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.login"))



@b_userobj.route('/prestartup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartupdashboard():
    if session.get("user") != None:
        return render_template("prestartup_dashboard.html",  title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.login"))





#         --  HOMEPAGES  --  THESE ARE THE USER HOMEPAGE ROUTES
@b_userobj.route('/ngo', methods = ("GET", "POST"), strict_slashes = False)
def ngo():
    return render_template('ngo.html')



@b_userobj.route('/prestartup', methods = ("GET", "POST"), strict_slashes = False)
def prestartup():
    return render_template('prestartup.html')



@b_userobj.route('/startup', methods = ("GET", "POST"), strict_slashes = False)
def startup():
    return render_template('startup.html')





#         --  OTHERS  --  THESE ARE THE USER OTHER ROUTES
@b_userobj.route('/donate', methods = ("GET", "POST"), strict_slashes = False)
def donate():
    return render_template('donate.html')



@b_userobj.route('/dashboard/donation', strict_slashes = False)
def dashboard_donation():
    return render_template('donation.html')









