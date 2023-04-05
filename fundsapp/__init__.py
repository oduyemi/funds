from flask import Flask
from flask import jsonify, render_template, request, session
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from fundsapp.admin import adminobj
from fundsapp.b_user import b_userobj
from fundsapp.i_user import i_userobj
from fundsapp.d_user import d_userobj
from fundsapp.models import db, B_user
from fundsapp.api import apiobj


# APPLICATION FACTORY TO AVOID CYCLIC IMPORTATION
def create_app():
    starter=Flask(__name__,instance_relative_config=True)
    from fundsapp import config
    # app.config.from_object(config.LiveConfig)
    starter.config.from_pyfile("config.py")
    from fundsapp.models import db
    db.init_app(starter) # NOT db
    csrf = CSRFProtect(starter)
    migrate = Migrate(starter,db)
    @starter.errorhandler(404)
    def page_not_found(e):
        id=session.get("b_user")
        user = db.session.query(B_user).filter(B_user.b_user_id==id).first()
        fname = db.session.query(B_user).filter(B_user.b_user_fname).first()
        lname = db.session.query(B_user).filter(B_user.b_user_lname).first()
        email = db.session.query(B_user).filter(B_user.b_user_email).first()
        return render_template("error404.html", fname=fname, lname=lname, email=email, user=user), 404

    @starter.errorhandler(500)
    def internal_server_error(e):
        return render_template("error500.html"), 500

    @starter.errorhandler(405)
    def method_not_allowed(e):
        if request.path.startswith('/api/'):
            return jsonify(message="Method Not Allowed"), 405
        else:
            return render_template("error405.html"), 405    
    starter.register_blueprint(adminobj)
    starter.register_blueprint(b_userobj)
    starter.register_blueprint(i_userobj)
    starter.register_blueprint(d_userobj)
    starter.register_blueprint(apiobj)
    return starter





