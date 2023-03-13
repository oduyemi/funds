import os, random, string, requests,json
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, jsonify
# from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.forms import LoginForm, SignupForm, RegistrationForm
from fundsapp.models import B_user, db, State, Industry, Business_type, Business, Business_disbursement

from . import b_userobj


def generate_name():
    global filename
    filename = random.sample(string.ascii_lowercase,10) #this will return a list
    return ''.join(filename) #here we join every member of the list "filename"





#         --  USERS: SESSION[B_USER] --  THESE ARE THE USER ROUTES
@b_userobj.route('/', methods = (["GET", "POST"]), strict_slashes = False)
def indexpage():
    return render_template('index.html', title = "Funds App")






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
        session['b_user']=userid
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
        session['b_user']=userid
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
        session['b_user']=userid
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
            #hashed = generate_password_hash(password)
            if email !="" and password !="":
                user = db.session.query(B_user).filter(B_user.b_user_email==email).first() 
                if user !=None:
                    pwd =user.b_user_password
                    chk = check_password_hash(pwd, password)
                    if chk:
                        userid = user.b_user_id
                        session['b_user'] = userid
                        return redirect(url_for('fbuser.startup'))
                    else:
                        flash('Invalid email or password', "danger")
                        return redirect(url_for('fbuser.startup_login'))
                else:
                    flash("Ensure that your login details are correct, or signup to create an account", "danger")  
                    return redirect(url_for('fbuser.startup_login'))     
        else:
            flash("You must complete all fields", "danger")
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
                        session['b_user'] = userid
                        db.session.add(user)
                        db.session.commit() 
                        return redirect(url_for('fbuser.ngo'))
                    else:
                        flash('Invalid email or password')
                        return redirect(url_for('fbuser.ngo_login'))
                else:
                    flash("Ensure that your login details are correct, or signup to create an account", "danger")  
                    return redirect(url_for('fbuser.ngo_login'))     
        else:
            flash("You must complete all fields", "danger")
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
                        session['b_user'] = userid
                        db.session.add(user)
                        db.session.commit() 
                        return redirect(url_for('fbuser.prestartup'))
                    else:
                        flash('Invalid email or password')
                        return redirect(url_for('fbuser.prestartup_login'))
                else:
                    flash("Ensure that your login details are correct, or signup to create an account", "danger")  
                    return redirect(url_for('fbuser.prestartup_login'))     
        else:
            flash("You must complete all fields", "danger")
            return redirect(url_for("fbuser.prestartup_signup"))
    

@b_userobj.route("/register", methods = ("GET", "POST"), strict_slashes = False)
def register():
    id = session.get("b_user")
    form = RegistrationForm()
    states = db.session.query(State).order_by(State.state_id).all()
    type = db.session.query(Business_type).order_by(Business_type.type_id).all()
    industries = db.session.query(Business).order_by(Business.business_industryid).all()

    #   Form Data
    bname = request.form.get("bname")
    phone = request.form.get("phone")
    email = request.form.get("email")
    website=request.form.get("website")
    address = request.form.get("address")
    state = request.form.get("state")
    btype = request.form.get("btype")
    bindustry = request.form.get("b_industry")
    regnumber = request.form.get("regnumber")
    tin = request.form.get("tin")
    b_desc = request.form.get("b_desc")
    pitch = request.form.get("pitch")
    

    if request.method == "GET":
        return render_template("register.html", form = form, states = states, type=type, industries=industries)
    else:
        if session.get("b_user") != None:
            if form.validate_on_submit:
                if bname =='' and phone == "" and email =='' and website =='' and address == "" and btype == "" and regnumber =='' and tin =='' and b_desc =='' and pitch =='' and bindustry == "" and state == "":
                    flash("Please fill all fields")
                    return redirect(url_for("fbuser.register"))    
                    
                else:                      
                    new_business=Business(business_name = bname,business_type = btype, business_email = email,business_state_id=state, business_phone_number =phone, business_website=website, business_address=address, business_rcnumber=regnumber, business_tin=tin,  business_desc=b_desc,business_pitch=pitch, business_industryid=bindustry, business_status_id=1, business_userid=id)
                    db.session.add(new_business)
                    db.session.commit()
                    return redirect(url_for("fbuser.reg2"))
        
        else:
            return redirect(url_for("fbuser.indexpage"))

@b_userobj.route("/registration", methods = ("GET", "POST"), strict_slashes = False)
def reg2():
    id = session.get("b_user")
    if id == None:
        return redirect("fbuser.indexpage")
    else:
        if request.method=='GET':
            return render_template("reg2.html")
        else:
            if session.get("b_user") != None:
                reg = request.files['reg']
                tax = request.files["tax"]
                plan = request.files["plan"]
                img1 = request.files["img1"]
                # img2 = request.files["img2"]
                # img3 = request.files["img3"]

                filename_reg = reg.filename 
                filetype_reg = reg.mimetype
                allowed1= ['.png','.jpg','.jpeg', '.pdf'] 

                filename_tax = tax.filename 
                filetype_tax = tax.mimetype 
                allowed2 = ['.png','.jpg','.jpeg', '.pdf']

                filename_plan = plan.filename 
                filetype_plan = plan.mimetype 
                allowed3 = ['.doc','.docx','.pdf', '.txt']

                filename_img1 = img1.filename 
                filetype_img1 = img1.mimetype 
                allowed4 = ['.png','.jpg','.jpeg', '.webp']

                # filename_img2 = img2.filename 
                # filetype_img2 = img2.mimetype 
                # allowed = ['.png','.jpg','.jpeg']

                # filename_img3 = img3.filename 
                # filetype_img3 = img3.mimetype 
                # allowed = ['.png','.jpg','.jpeg']

                if filename_reg !="":
                    name,ext = os.path.splitext(filename_reg) 
                    if ext.lower() in allowed1: 
                        newname_reg = generate_name()+ext
                        reg.save("fundsapp/static/uploads/"+newname_reg) 
                    else:
                        return "File not allowed!"
                else:
                    flash("Please choose a File")

                if filename_tax!="":
                    name,ext = os.path.splitext(filename_tax) 
                    if ext.lower() in allowed2: 
                        newname_tax = generate_name()+ext
                        tax.save("fundsapp/static/uploads/"+newname_tax) 
                    else:
                        return "File not allowed!!"
                else:
                    flash("Please choose a File")

                if filename_plan !="":
                    name,ext = os.path.splitext(filename_plan) 
                    if ext.lower() in allowed3: 
                        newname_plan = generate_name()+ext
                        plan.save("fundsapp/static/uploads/"+newname_plan) 
                    else:
                        return "File not allowed!!!"
                else:
                    flash("Please choose a File")
            
                if filename_img1 !="":
                    name,ext = os.path.splitext(filename_img1) 
                    if ext.lower() in allowed4: 
                        newname_img1 = generate_name()+ext
                        img1.save("fundsapp/static/uploads/"+newname_img1) 
                    else:
                        flash("Images only!")
                else:
                    flash("Please choose a File") 

            buzz=f"UPDATE business SET business_reg_file = '{newname_reg}', business_tin_file = '{newname_tax}', business_plan = '{newname_plan}', business_img1 = '{newname_img1}' WHERE business_userid = '{id}'"
            result = db.session.execute(text(buzz))
            db.session.commit()
            flash('Business registration successfully completed')
            return redirect(url_for('fbuser.user_profile'))



@b_userobj.route('/signout', methods = ("GET", "POST"), strict_slashes = False)
def signout():
    if session.get("b_user") != None:
        session.pop("b_user", None)
    return redirect(url_for("fbuser.indexpage"))  





#         --  DASHBOARDS  --  THESE ARE THE USER DASHBOARD ROUTES
@b_userobj.route('/dashboardlayout', methods = ("GET", "POST"), strict_slashes = False)
def dashboard():
    id=session.get("b_user")
    user = db.session.query(B_user).first()
    state = db.session.query(State).order_by(State.state_id).all()
    reg = db.session.query(Business).where(Business.business_type==1).all()
    pend =  db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
    app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
    fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==1).all()
    content = db.session.query(Business).where(Business.business_type==1,Business.business_status_id==2).order_by(Business.business_name,Business.business_userid,Business.business_state_id)
    registered = len(reg)
    pending = len(pend)
    approved = len(app)
    funded = len(fund)
    return render_template("dashboardlayout.html", registered=registered, pending=pending, approved=approved,content=content, id=id,
    funded=funded, user=user, state=state, title = "Dashboard - Funds App")


@b_userobj.route('/ngo/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngodashboard():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==1).all()
        pend =  db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==1).all()
        content = db.session.query(Business).where(Business.business_type==1,Business.business_status_id==2).order_by(Business.business_name,Business.business_userid,Business.business_state_id)
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("ngo_dashboard.html", registered=registered, pending=pending, approved=approved,content=content,
        funded=funded, user=user, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/ngolist/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngolist():
    id = session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==1).all()
        pend =  db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==3).all()
        query = f"SELECT * from business WHERE business_type=1 and (business_status_id=1 or business_status_id=2)"
        content = db.session.execute(text(query))
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("ngolist.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/ngocontact/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngocontact():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==3).all()
        query = f"SELECT * from b_user join business WHERE business_status_id=1"
        content = db.session.execute(text(query))
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("ngocontact.html", registered=registered, pending=pending, approved=approved, content=content,
        funded=funded, user=user, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/ngoaccount/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngoaccount():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
        pend =  db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        query = f"SELECT business_name, industry_name, business_desc, business_email from business JOIN industry ON business_id JOIN b_user on business_id WHERE business_type=1 AND business_status_id=2 AND industry_id=business_industryid ORDER BY business_id"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==3).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("ngoaccount.html", registered=registered, pending=pending, approved=approved, content=content,
        funded=funded, user=user, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/ngopitch/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def ngopitch():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==1).all()
        pend =  db.session.query(Business).where(Business.business_type==1, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==1, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==3).all()
        content = db.session.query(Business).where(Business.business_type==1,Business.business_status_id==2).order_by(Business.business_name,Business.business_userid,Business.business_state_id)
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("ngopitch.html", registered=registered, pending=pending, approved=approved,content=content,
        funded=funded, user=user, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))





@b_userobj.route('/startup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startupdashboard():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        industry = db.session.query(Industry).order_by(Industry.industry_id).all()
        reg = db.session.query(Business).where(Business.business_type==2).all()
        pend =  db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        query = f"SELECT * from business WHERE business_type=2 and business_status_id=2"
        content = db.session.execute(text(query))
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("startup_dashboard.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, industry = industry, content=content, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.startup_login"))

@b_userobj.route('/startuppitch/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startuppitch():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==2).all()
        pend =  db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE business_type=2 and business_status_id=2"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("startuppitch.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/startuplist/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startuplist():
    id=session.get("b_user")
    if id != None:
        state = db.session.query(State).order_by(State.state_id).all()
        user = db.session.query(B_user).first()
        reg = db.session.query(Business).where(Business.business_type==2).all()
        pend =  db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE business_type=2 and (business_status_id=1 or business_status_id=2)"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("startuplist.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/startupcontact/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startupcontact():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        userid = db.session.query(B_user).filter(B_user.b_user_id).all()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==2).all()
        pend =  db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        query = f"SELECT * from b_user JOIN business ON business_id WHERE business_id = b_user_business"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("startupcontact.html", registered=registered, pending=pending, approved=approved, userid=userid,
        funded=funded,content=content, user=user, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/startupaccount/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def startupaccount():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==2).all()
        pend =  db.session.query(Business).where(Business.business_type==2, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==2, Business.business_status_id==2).all()
        query = f"SELECT business_name, industry_name, business_desc, business_email from business JOIN industry ON business_id WHERE business_type=2 AND business_status_id=2 AND industry_id=business_industryid ORDER BY business_id"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("startupaccount.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))




@b_userobj.route('/prestartup/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartupdashboard():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        industry = db.session.query(Industry).order_by(Industry.industry_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==3).all()
        query = f"SELECT * from business WHERE business_type=3 and business_status_id=2"
        content = db.session.execute(text(query))
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("prestartup_dashboard.html", registered=registered, pending=pending, approved=approved, content=content,
        funded=funded, user=user, industry = industry, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.prestartup_login"))

@b_userobj.route('/prestartuppitch/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartuppitch():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE business_type=3 and business_status_id=2"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("prestartuppitch.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/prestartuplist/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartuplist():
    session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE business_type=3 and (business_status_id=1 or business_status_id=2)"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("prestartuplist.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/prestartupcontact/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartupcontact():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT * from business WHERE business_type=3 and business_status_id=2"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("prestartupcontact.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))

@b_userobj.route('/prestartupaccount/dashboard', methods = ("GET", "POST"), strict_slashes = False)
def prestartupaccount():
    id=session.get("b_user")
    if id != None:
        user = db.session.query(B_user).first()
        state = db.session.query(State).order_by(State.state_id).all()
        reg = db.session.query(Business).where(Business.business_type==3).all()
        pend =  db.session.query(Business).where(Business.business_type==3, Business.business_status_id==1).all()
        app = db.session.query(Business).where(Business.business_type==3, Business.business_status_id==2).all()
        query = f"SELECT business_name, industry_name, business_desc, business_email from business JOIN industry ON business_id JOIN b_user on business_id WHERE business_type=3 AND business_status_id=2 AND industry_id=business_industryid ORDER BY business_id"
        content = db.session.execute(text(query))
        fund = db.session.query(Business_disbursement).order_by(Business_disbursement.business_id).where(Business_type==2).all()
        registered = len(reg)
        pending = len(pend)
        approved = len(app)
        funded = len(fund)
        return render_template("prestartupaccount.html", registered=registered, pending=pending, approved=approved,
        funded=funded, user=user, content=content, state=state, title = "Dashboard - Funds App")
    else:
        return redirect(url_for("fbuser.ngo_login"))






#         --  HOMEPAGES  --  THESE ARE THE USER HOMEPAGE ROUTES
@b_userobj.route('/ngo', methods = ("GET", "POST"), strict_slashes = False)
def ngo():
    id=session.get("b_user")
    user = db.session.query(B_user).first()
    return render_template('ngo.html',  user=user)



@b_userobj.route('/prestartup', methods = ("GET", "POST"), strict_slashes = False)
def prestartup():
    id=session.get("b_user")
    user = db.session.query(B_user).first()
    return render_template('prestartup.html',  user=user)



@b_userobj.route('/startup', methods = ("GET", "POST"), strict_slashes = False)
def startup():
    id=session.get("b_user")
    user = db.session.query(B_user).first()
    return render_template('startup.html',  user=user)



@b_userobj.route('/business/account/<id>', methods = ("GET", "POST"), strict_slashes = False)
def b_account(id):
    business_deets= Business.query.get_or_404(id)
    return render_template("b_account.html", business_deets=business_deets)







#         --  DROPDOWNS  --  THESE ARE JSON REQUESTS HANDLED TO POPULATE DROPDOWN MENUS











#         --  OTHERS  --  THESE ARE THE USER OTHER ROUTES
@b_userobj.route('/profile/<cid>', methods=["POST","GET"], strict_slashes = False)
def user_profile(cid):
    id = session.get('b_user')
    user = db.session.query(B_user).first()
    deets = db.session.query(B_user).filter(B_user.b_user_id==cid).first()
    contact = db.session.query(Business).join(B_user, Business.bdeets).where(Business.business_userid==cid).first()
    if id ==None:
        return redirect(url_for('fbuser.indexpage'))
    else:
        if request.method =="GET":
            return render_template('profile.html', deets=deets, userid=id, contact=contact, user=user)
        else: #form was submitted
            userobj = db.session.query(B_user).get(id)
            db.session.commit()
            return redirect(url_for("fbuser.user_profile"))

@b_userobj.route('/profile/picture', methods=["POST","GET"])
def profile_picture():
    id= session.get("b_user")
    if id == None:
        return redirect(url_for('fbuser.startup_login'))
    else:
        if request.method == 'GET':
            return render_template('profile_picture.html')
        else:
            file = request.files['pix']
            filename = file.filename 
            filetype = file.mimetype 
            allowed = ['.png','.jpg','.jpeg','.webp']
            if filename !="":
                name,ext = os.path.splitext(filename) 
                if ext.lower() in allowed: 
                    newname = generate_name()+ext
                    file.save("fundsapp/static/uploads/"+newname) 
                    userpic=f"UPDATE b_user SET b_user_pic = '{newname}' WHERE (b_user_id='{id}')"
                    result = db.session.execute(text(userpic))
                    db.session.commit()
                    return redirect(url_for('fbuser.startupdashboard'))
                else:
                    return "Images only!"
            else:
                flash("Please choose a File")
                return redirect("fbuser.user_profile")


@b_userobj.route('/account/<bid>', methods=["POST","GET"], strict_slashes = False)
def b_profile(bid):
    id = session.get('b_user')
    user = db.session.query(B_user).first()
    deets = db.session.query(State).filter(State.state_id==bid).first()
    contact = db.session.query(Business).join(B_user, Business.bdeets).where(Business.business_userid==bid).first()
    if id ==None:
        return redirect(url_for('fbuser.indexpage'))
    else:
        if request.method =="GET":
            return render_template('account.html', deets=deets, userid=id, contact=contact,user=user)
        else: 
            bobj = db.session.query(Business).get(id)
            db.session.commit()
            return redirect(url_for("fbuser.b_profile"))



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



