from flask import render_template, redirect, flash, session, request
from sqlalchemy.sql import text

from werkzeug.security import generate_password_hash, check_password_hash

from fundsapp import starter, db

starter.route("/admin", methods=["POST", "GET"])
def admin_home():
    if request.method == "GET":
        return render_template("admin/adminreg.html")
    else:
        username = request.form.get("username")
        pwd = request.form.get(pwd)
        """Convert the plain password to hashed value and insert into db"""
        hashed_pwd = generate_password_hash(pwd)
        if username != "" or pwd != "":
            query = f"INSERT INTO admin SET admin_username = '{username}', admin_pwd = '{hashed_pwd}'"
            db.session.execute(text(query))
            db.session.commit()
            flash("Registration Successful. Login Here")
            return redirect("/admin")
        else:
            return redirect('admin/home')
        
@starter.route('/investment/dashboard')
def admin_dashboard():
    return "Dashboard"
        
        
    