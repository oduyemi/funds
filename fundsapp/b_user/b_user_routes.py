import os, random, string
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from fundsapp.models import B_user, db, Lga, State, Industry, Business_type

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
    def validate_email(self,email):
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")






#         --  USERS: SESSION[USER] --  THESE ARE THE USER ROUTES
@b_userobj.route('/', methods = (["GET", "POST"]), strict_slashes = False)
def indexpage():
    return render_template('index.html', title = "Funds App")



@b_userobj.route("/home", methods = ("GET", "POST"), strict_slashes = False)
def home():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template("home.html", dp = dp, fname =fname, lname = lname, email=email, title = "Homepage - Funds App")



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
    if request.method=='GET':
        return render_template('login.html', title="Login", form=form)
    else:
        if form.validate_on_submit:
            email = form.email.data
            password = form.password.data
            hashed = generate_password_hash(password)
            if email !="" and password !="":
                user = db.session.query(B_user).filter(B_user.b_user_email==email).first() 
                if user !=None:
                    pwd =user.b_user_password
                    chk = check_password_hash(pwd, password)
                    if chk:
                        userid = user.b_user_id
                        session['user'] = userid
                        db.session.add(user)
                        db.session.commit() 
                        return redirect(url_for('fbuser.startupdashboard'))
                    else:
                        flash('Invalid password')
                        return redirect(url_for('fbuser.login'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("fbuser.signup"))



    

@b_userobj.route("/register", methods = ("GET", "POST"), strict_slashes = False)
def register():
    form = RegistrationForm()
    state = db.session.query(State).order_by(State.state_id).all()
    type = db.session.query(Business_type).order_by(Business_type.type_id).all()
    if form.validate_on_submit():
        email = request.form.get('email')
        msg = request.form.get('message')
        #insert into database and send the feedback to AJAX/Javascript
        return f"{email} and {msg}"
    else:
        return render_template("register.html", form = form, state = state, type = type)



@b_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
#@login_required
def signout():
    #logout_user()
    if session.get("user") == None:
        session.pop("user", None)
    return redirect(url_for("fbuser.login"))  





#         --  DASHBOARDS  --  THESE ARE THE USER DASHBOARD ROUTES
@b_userobj.route('/dashboardlayout', methods = ("GET", "POST"), strict_slashes = False)
def dashboardlayout():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template("ngo_dashboard.html", dp = dp, fname = fname, lname = lname, email = email,  title = "Dashboard - Funds App")
    


@b_userobj.route('/ngo/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngodashboard():
    if session.get("user") != None:
        dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
        fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
        lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
        email = db.session.query(B_user).filter(B_user.b_user_email).first()
        query = (f"SELECT * FROM state ORDER BY state_id")
        result = db.session.execute(text(query))
        state = result.fetchall()
        return render_template("ngo_dashboard.html", dp = dp, fname =fname, lname = lname, email=email, state = state,  title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.login"))



@b_userobj.route('/startup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startupdashboard():
    if session.get("user") != None:
        dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
        fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
        lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
        email = db.session.query(B_user).filter(B_user.b_user_email).first()
        industry = db.session.query(Industry).order_by(Industry.industry_id).all()
        return render_template("startup_dashboard.html", dp = dp, fname =fname, lname = lname, email=email, industry = industry, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.login"))



@b_userobj.route('/prestartup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartupdashboard():
    if session.get("user") != None:
        dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
        fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
        lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
        email = db.session.query(B_user).filter(B_user.b_user_email).first()
        industry = db.session.query(Industry).order_by(Industry.industry_id).all()
        return render_template("prestartup_dashboard.html", dp = dp, fname =fname, lname = lname, email=email, industry = industry, title = "Dashboard - Funds App")
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





#         --  DROPDOWNS  --  THESE ARE JSON REQUESTS HANDLED TO POPULATE DROPDOWN MENUS
@b_userobj.route("/load_lga", methods = ["POST", 'GET'])
def load_state():
    if request.method == "POST":
        stateid = request.form["state_id"]
        print(stateid)
        query = (f"SELECT * FROM lga WHERE state_id = %s ORDER BY lga_name ASC" [stateid])
        result = db.session.execute(text(query))
        state_lga =  result.fetchall()
        outputData = []
        for row in Lga:
            outputObj = {
                "id":row["state_id"],
                "name":row["lga_name"]
            }
            outputData.append(outputObj)
        return jsonify(outputData)

    #state = db.session.query(State).filter(State.state_name).all()
    data = "<select class='form-control border-success'>"
    for s in State:
        data2send = data + "<option>"+s.state_name + "</option>"
    data2send = {data + "</select>"}
    # stateid = request.args.get("stateid")
    return jsonify(data2send)



@b_userobj.route("/load_lga/<stateid>")
def load_lga(stateid):
    lgas = db.session.query(Lga).filter(Lga.lga_stateid==stateid).all()
    data2send = "<select class='form-control border-success'>"
    for s in lgas:
        data2send = data2send+"<option>"+s.lga_name +"</option>"
    data2send = data2send + "</select>"
    # stateid = request.args.get("stateid")
    return data2send


@b_userobj.route("/load_industry")
def load_industry():
    # dataGet = request.get_json(force = True)
    # state = db.session.query(State).filter(State.state_name).all()
    # data = "<select class='form-control border-success'>"
    # for s in State:
    #     data2send = data + "<option>"+s.state_name + "</option>"
    # data2send = {data + "</select>"}
    # # stateid = request.args.get("stateid")
    # return jsonify(data2send)
    return "done"










#         --  OTHERS  --  THESE ARE THE USER OTHER ROUTES
@b_userobj.route('/donate', methods = ("GET", "POST"), strict_slashes = False)
def donate():
    return render_template('donate.html')



@b_userobj.route('/dashboard/donation', strict_slashes = False)
def dashboard_donation():
    return render_template('donation.html')



