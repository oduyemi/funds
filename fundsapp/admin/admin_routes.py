import os, random, string
from flask import render_template,redirect,request,session,flash,abort,url_for
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from fundsapp.models import db, Admin,Business,Contact
from fundsapp.forms import DonorLoginForm, DonorSignupForm

from . import adminobj





@adminobj.route("/login", methods = ("GET", "POST"), strict_slashes = False)
def adminlogin():
    if request.method == "GET":
       return render_template('adminlogin.html', title="Login")
    else:
        username = request.form.get("username") 
        password = request.form.get("pwd") 
        if username !="" and password !="":
            adm = db.session.query(Admin).filter(Admin.admin_username==username, Admin.admin_pwd==password).first() 
            if adm !=None:
                userid = adm.admin_id
                session['admin_'] = userid
                db.session.add(adm)
                db.session.commit() 
                return redirect(url_for('bpadmin.admindashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('bpadmin.adminlogin'))
        else:
            flash("You must complete all fields")


@adminobj.route("/")
def home():
    return redirect(url_for("bpadmin.adminlogin"))


@adminobj.route("/dashboard")
def admindashboard():
    if session.get('admin_') != None:
        bdeets=db.session.query(Business).where(Business.business_status_id==1).all()
        return render_template("admindashboard.html", bdeets=bdeets)
    else:
        return redirect("/admin/login")

@adminobj.route("/approved")
def approve():
    if session.get('admin_') != None:
        bdeets=db.session.query(Business).where(Business.business_status_id==2).all()
        return render_template('approved.html',bdeets=bdeets)

@adminobj.route("/declined")
def decline():
    if session.get('admin_') != None:
        bdeets=db.session.query(Business).where(Business.business_status_id==3).all()
        return render_template('declined.html',bdeets=bdeets)

@adminobj.route("/pending")
def pending():
    if session.get('admin_') != None:
        bdeets=db.session.query(Business).where(Business.business_status_id==1).all()
        return render_template('pending.html',bdeets=bdeets)

@adminobj.route("/registered")
def registered():
    if session.get('admin_') != None:
        bdeets=db.session.query(Business).order_by(Business.business_id).all()
        return render_template('pending.html',bdeets=bdeets)


@adminobj.route("/logout")
def adminlogout():
    if session.get("admin_") != None:
        session.pop("admin_",None)
    return redirect('/admin/login')


@adminobj.route('/profile/delete/<id>')
def delete_profile(id):
    bobj = Business.query.get_or_404(id)
    db.session.delete(bobj)
    db.session.commit()
    flash("Successfully deleted!")
    return redirect(url_for("bpadmin.admindashboard"))

@adminobj.route('/alltopics')
def all_topics():
    if session.get('admin_') == None:
        return redirect("/login")
    else:
        # topicsall = db.session.query(Topics).all()
        alltopics = Contact.query.all()
        return render_template("alltopics.html",alltopics=alltopics)

@adminobj.route('/admin/topic/edit/<id>')
def edit_topic(id):
    if session.get('admin_') !=None:
        topic_deets = Contact.query.get(id)
        return render_template('edit_topic.html',topic_deets=topic_deets)
    else:
        return redirect(url_for("login"))

@adminobj.route("/admin/update_topic", methods=["POST"])
def update_status():
    if session.get('admin_') !=None:
        newstatus = request.form.get('status')
        statusid = request.form.get('statusid')
        s = Business.query.get(statusid)
        s.business_status_id = newstatus
        db.session.commit()
        flash("'Status' successfully updated")
        return redirect(url_for("bpadmin.admindashboard"))
    else:
        return redirect("/admin/login")


