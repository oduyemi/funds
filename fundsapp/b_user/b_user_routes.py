import os, random, string, requests,json
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField,TextAreaField, SelectField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from fundsapp.models import B_user, db, Lga, State, Industry, Business_type, Business

from . import b_userobj




def generate_name():
    filename = random.sample(string.ascii_lowercase,10) #this will return a list
    return ''.join(filename) #here we join every member of the list "filename"




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
    bname = StringField("bname",
    validators=[
        DataRequired(),
        length(min=3, max=50, message = "Please provide a valid name"),
        Regexp(
            "^[A-Za-z] [A-Za-a0-9.]*", 0, "Your name must contain only letters"
            ),
        ],
            render_kw={"placeholder": "Enter your business name"})
    phone = StringField("phone",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid phone number"),
        Regexp(
            "^[A-Za-z] [A-Za-a0-9.]*", 0, "Enter your phone number in its appropriate format"
            ),
        ],
            render_kw={"placeholder": "Enter your business phone number"})

    email = StringField("email",
        validators=
            [DataRequired(),
            Email()],
            render_kw={"placeholder": "Enter your business email address"})
    
    
    website = StringField("website",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid url"),
            Regexp(
                "^[www.] [A-Za-a0-9.]*", 0, "Your Last name must contain only letters")],
        render_kw={"placeholder": "Enter your website url"})
    
    
    address = TextAreaField("address",
         validators=[
            DataRequired(),
            length(min=1, max=120, message = "Please provide a valid address")],
        render_kw={"placeholder": "Enter your Address"})
    
    state = SelectField("state",
        validators=[
            DataRequired()]),
    
    lga = SelectField("lga",
        validators=[
            DataRequired()]),
    
    btype = SelectField("btype",
            validators=[
            DataRequired()]),

    b_industry = SelectField("b_industry",
        validators=[
            DataRequired()]),       

    regnumber = StringField("regnumber",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid number"),
        Regexp(
            "^[A-Za-z] [A-Za-a0-9.]*", 0, "Please provide a valid number"
            ),
        ],
            render_kw={"placeholder": "Enter your BN or RC number"})

    regfile = FileField("regfile",
            validators=[
            DataRequired(),
            length(min=5, max=100)])

    tin = StringField("tin",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid number")],
            render_kw={"placeholder": "Enter your tax number"})

    
    taxfile = FileField("taxfile",
            validators=[
            DataRequired(),
            length(min=5, max=100)])
    
    b_desc = TextAreaField("b_desc",
         validators=[
            DataRequired(),
            length(min=1, max=800)])
    
    pitch = StringField("pitch",
        validators=[
            DataRequired(),
            length(min=1, max=800)])

    planfile = FileField("planfile",
        validators=[
            DataRequired(),
            length(min=5, max=100)])
    
    img1 = FileField("img1",
        validators=[
            DataRequired(),
            length(min=5, max=100)])
    
    img2 = FileField("img2",
        validators=[
            DataRequired(),
            length(min=5, max=100)])
    
    
    img3 = FileField("img3",
        validators=[
            DataRequired(),
            length(min=5, max=100)])

    submit = SubmitField("Submit")
    
    def validate_email(self, email):
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")    
    def validate_email(self,email):
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")






#         --  USERS: SESSION[USER] --  THESE ARE THE USER ROUTES
@b_userobj.route('/', methods = (["GET", "POST"]), strict_slashes = False)
def indexpage():
    return render_template('index.html', title = "Funds App")



"""@b_userobj.route("/home", methods = ("GET", "POST"), strict_slashes = False)
def home():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template("home.html", dp = dp, fname =fname, lname = lname, email=email, title = "Homepage - Funds App")"""



# @b_userobj.route("/profile", methods=['POST', 'GET'], strict_slashes = False)
# def profile():
#     id = session.get('user')
#     if id ==None:
#         return redirect(url_for('fbuser.login'))
#     else:
#         if request.method =='GET':
#             deets = db.session.query(B_user).filter(B_user.b_user_id==id).first()
#             return render_template('profile.html',deets=deets)
#         else:
#             #form was submitted
#             #To do: retrieve from data (fullname and phone), save them in respective variables 
#             fname = request.form.get('fname')
#             lname = request.form.get('lname')
#             email = request.form.get('email')
#             #update query
#             userobj = db.session.query(B_user).get(id)
#             userobj.b_user_fname=fname
#             userobj.b_user_lname=lname
#             userobj.user_email =email
#             db.session.commit()
#             flash('Profile Updated')
#             return redirect(url_for('fbuser.dashboard'))





#         --  FORM AUTHENTICATION  --  THESE ARE THE USER FORM ROUTES AND AUTHENITCATION
@b_userobj.route('/startup/signup', methods = ["GET", "POST"], strict_slashes = False)
def startup_signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template('startup_signup.html', title="Sign Up", form = form)
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
        return redirect(url_for('fbuser.startup_login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('fbuser.startup_signup'))


@b_userobj.route('/prestartup/signup', methods = ["GET", "POST"], strict_slashes = False)
def prestartup_signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template('prestarup_signup.html', title="Sign Up", form = form)
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
        return redirect(url_for('fbuser.prestartup_login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('fbuser.prestartup_signup'))

@b_userobj.route('/ngo/signup', methods = ["GET", "POST"], strict_slashes = False)
def ngo_signup():
    form = SignupForm()
    if request.method == "GET":
        return render_template('ngo_signup.html', title="Sign Up", form = form)
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
        return redirect(url_for('fbuser.ngo_login'))
    else:
        flash('You must fill the form correctly to signup', "danger")
        return redirect(url_for('fbuser.ngo_signup'))

@b_userobj.route('/startup/login', methods = (["GET", "POST"]), strict_slashes = False)
def startup_login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('startup_login.html', title="Login", form=form)
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
                        flash('Invalid email or password')
                        return redirect(url_for('fbuser.startup_login'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("fbuser.startup_signup"))



@b_userobj.route('/ngo/login', methods = (["GET", "POST"]), strict_slashes = False)
def ngo_login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('ngo_login.html', title="Login", form=form)
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
                        return redirect(url_for('fbuser.ngodashboard'))
                    else:
                        flash('Invalid email or password')
                        return redirect(url_for('fbuser.ngo_login'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("fbuser.ngo_signup"))


@b_userobj.route('/prestartup/login', methods = (["GET", "POST"]), strict_slashes = False)
def prestartup_login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('prestartup_login.html', title="Login", form=form)
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
                        return redirect(url_for('fbuser.prestartupdashboard'))
                    else:
                        flash('Invalid email or password')
                        return redirect(url_for('fbuser.prestartup_login'))
            else:
                flash("You must complete all fields")
                return redirect(url_for("fbuser.prestartup_signup"))
    

@b_userobj.route("/register", methods = ("GET", "POST"), strict_slashes = False)
def register():
    form = RegistrationForm()
    states = db.session.query(State).order_by(State.state_id).all()
    type = db.session.query(Business_type).order_by(Business_type.type_id).all()
    industries = db.session.query(Business).order_by(Business.business_industryid).all()
    bname = form.bname.data
    phone = form.phone.data
    email = request.form.get("email")
    website=request.form.get("website")
    address = request.form.get("address")
    state = request.form.get("state")
    lga = request.form.get("lga")
    btype = request.form.get("btype")
    bindustry = request.form.get("b_industry")
    regnumber = request.form.get("regnumber")
    tin = request.form.get("tin")
    taxfile = request.files("taxfile")
    b_desc = request.form.get("b_desc")
    pitch = request.form.get("pitch")
    planfile = request.files("planfile")
    img1 = request.files("img1")
    img2 = request.files("img2")
    img3 = request.files("img3")
    lga = db.session.query(Lga).order_by(Lga.lga_stateid).all()
    if request.method == "GET":
        return render_template("register.html", form = form, states = states, type=type, lga=lga, industries=industries)
    else:
        if session.get("user") != None:
            if form.validate_on_submit:
                if bname =='' and phone == "" and email =='' and website =='' and address == "" and btype == "" and regnumber =='' and tin =='' and taxfile == "" and b_desc =='' and pitch =='' and planfile == "" and img1 =='' and img2 =='' and img3 == "" and bindustry == "":
                    flash("Please fill all fields")
                    return redirect(url_for("fbuser.register"))    
                    
                else:  
                    new_business=Business(business_name = bname, business_type = btype, business_email = email, Business_type=btype, business_state_id=state, business_lga_id=lga, business_phone_number =phone, business_website=website, business_address=address, business_rcnumber=regnumber, business_tin=tin, business_tin_file=taxfile, business_desc=b_desc,business_pitch=pitch, business_plan=planfile, business_industryid=bindustry, business_img1=img1,business_img2=img2,business_img3=img3, business_status_id=1)
                    db.session.add(new_business)
                    db.session.commit()
                    flash("Successfully Registered")
                    return redirect(url_for("fbuser.profile"))
        
        else:
            return redirect(url_for("fbuser.indexpage"))



@b_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
def signout():
    #logout_user()
    if session.get("user") != None:
        session.pop("user", None)
    return redirect(url_for("fbuser.indexpage"))  





#         --  DASHBOARDS  --  THESE ARE THE USER DASHBOARD ROUTES
'''@b_userobj.route('/dashboardlayout', methods = ("GET", "POST"), strict_slashes = False)
def dashboardlayout():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).join(State).filter(B_user.b_user_lname, State.state_id).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template("ngo_dashboard.html", dp = dp, fname = fname, lname = lname, email = email,  title = "Dashboard - Funds App")
    '''


@b_userobj.route('/ngo/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngodashboard():
    if session.get("user") != None:
        dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
        fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
        lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
        location = db.session.query(State).order_by(State.state_id).all()
        email = db.session.query(B_user).filter(B_user.b_user_email).first()
        query = (f"SELECT * FROM state ORDER BY state_id")
        result = db.session.execute(text(query))
        state = result.fetchall()
        return render_template("ngo_dashboard.html", dp = dp, fname =fname, lname = lname, email=email, location=location, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))



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
        return redirect(url_for("fbuser.startup_login"))



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
        return redirect(url_for("fbuser.prestartup_login"))





#         --  HOMEPAGES  --  THESE ARE THE USER HOMEPAGE ROUTES
@b_userobj.route('/ngo', methods = ("GET", "POST"), strict_slashes = False)
def ngo():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template('ngo.html',  dp = dp, fname =fname, lname = lname, email=email,)



@b_userobj.route('/prestartup', methods = ("GET", "POST"), strict_slashes = False)
def prestartup():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template('prestartup.html',  dp = dp, fname =fname, lname = lname, email=email,)



@b_userobj.route('/startup', methods = ("GET", "POST"), strict_slashes = False)
def startup():
    dp = db.session.query(B_user).filter(B_user.b_user_pic).first()
    fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
    lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
    email = db.session.query(B_user).filter(B_user.b_user_email).first()
    return render_template('startup.html',  dp = dp, fname =fname, lname = lname, email=email)



@b_userobj.route('/business/account/<id>', methods = ("GET", "POST"), strict_slashes = False)
def b_account(id):
    business_deets= Business.query.get_or_404(id)
    return render_template("b_account.html", business_deets=business_deets)







#         --  DROPDOWNS  --  THESE ARE JSON REQUESTS HANDLED TO POPULATE DROPDOWN MENUS
@b_userobj.route("/load_lga/<stateid>")
def load_lga(stateid):
    lgas = db.session.query(Lga).filter(Lga.lga_stateid==stateid).all()
    data2send = "<select class='form-select border-success'>"
    for s in lgas:
        data2send = data2send+"<option>"+s.lga_name +"</option>"
    
    data2send = data2send + "</select>"

    return data2send

@b_userobj.route("/loadngo")
def load_ngo():
    ngoorg= (f"SELECT business_name FROM business where business_status_id=2 and business_type=2")
    ngo_place = (f"SELECT state from business where business_status_id=2 and business_type=2 ORDER_BY business_state_id")
    ngo_person = (f"SELECT b_user_fame b_user_lname from business order_by business_userid where business_status_id=2 and business_type=2")
    data = [ngoorg, ngo_person, ngo_place]
    return jsonify(data)
    # return {
    #     "info1": ["Erekere Tours", "Ayodele Awoyemi", "Lagos"],
    #     "info2": ["WeMove Logistics", "Joy Garba", "Kaduna"]
    # }
    # ngo_name = db.session.query(Business).filter(Business.business_name).where(Business.business_status_id==2, Business.business_type==1).order_by(Business.business_id).all()
    # #ngo_place = db.session.query(Business).filter(Business.business_state_id).where(Business.business_status_id==2, Business.business_type==1).order_by(Business.business_id).all()
    # url= "/ngo/dashboard"
    # data = {"n_name": "ngo_name"}
    # headers = {"Accept" : "application/json"}
    # output2 = requests.post(url, data = data, headers = headers)
    # return json.dumps(output2)
    # ngo_name = db.session.query(Business).filter(Business.business_name).where(Business.business_status_id==2, Business.business_type==1).order_by(Business.business_id).all()
    # ngo_place = db.session.query(Business).filter(Business.business_state_id).where(Business.business_status_id==2, Business.business_type==1).order_by(Business.business_id).all()
    # ngo_person = db.session.query(Business).filter(Business.business_userid).where(Business.business_status_id==2, Business.business_type==1).order_by(Business.business_id).all()
    # n_info = {
    # "n_name": "ngo_name",
    # "n_person": "ngo_person",
    # "n_state": "ngo_place"
    # }
    # data = json.dumps(n_info)
    # return jsonify(data)











#         --  OTHERS  --  THESE ARE THE USER OTHER ROUTES
@b_userobj.route('/profile',methods=["POST","GET"])
def profile():
    id = session.get('user')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    phoneNumber = request.form.get('number')
    if id ==None:
        return redirect(url_for('fbuser.login'))
    else:
        if request.method =="GET":
            deets = db.session.query(B_user).filter(B_user.b_user_id==id).first()
            return render_template('profile.html', deets=deets, fname=fname, lname=lname, email=email, phoneNumber=phoneNumber)
        else: #form was submitted
            userobj = db.session.query(B_user).get(id)
            userobj.user_fname = fname
            userobj.user_email = email
            db.session.commit()
            flash("Profile Updated!")
            return redirect("/profile")

@b_userobj.route('/profile/picture', methods=["POST","GET"])
def profile_picture():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    if session.get('user') == None:
        return redirect(url_for('fbuser.login'))
    else:
        if request.method == 'GET':
            return render_template('profile_picture.html', fname=fname, lname=lname, email=email)
        else:
            #retrieve the file
            file = request.files['pix']

            filename = file.filename 
            filetype = file.mimetype 
            allowed = ['.png','.jpg','.jpeg']
            if filename !="":
                name,ext = os.path.splitext(filename) 
                if ext.lower() in allowed: 
                    newname = generate_name()+ext
                    file.save("fundsapp/static/uploads/"+newname) 
                    # user = db.session.query(User).get(id)
                    # user.user_pix = newname
                    db.session.commit()
                    return redirect(url_for('dashboard'))
                else:
                    return "File not allowed"
            else:
                flash("Please choose a File")
                return "Form was submitted here"
@b_userobj.route('/donate', methods = ("GET", "POST"), strict_slashes = False)
def donate():
    return render_template('donate.html')



@b_userobj.route('/dashboard/donation', strict_slashes = False)
def dashboard_donation():
    return render_template('donation.html')



@b_userobj.route("/privacy-policy", strict_slashes = False)
def policy():
    return render_template("privacy-policy.html")    



@b_userobj.route("/terms", strict_slashes = False)
def terms():
    return render_template("terms.html")    



