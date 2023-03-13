
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db=SQLAlchemy()



class Business(db.Model): 
    business_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(150), nullable=True) 
    business_type = db.Column(db.Integer(),db.ForeignKey('business_type.type_id'))
    business_industryid = db.Column(db.Integer(),db.ForeignKey('industry.industry_id'))
    business_address = db.Column(db.String(255), nullable=True)
    business_state_id = db.Column(db.Integer(),db.ForeignKey('state.state_id'))
    business_email  = db.Column(db.String(100), unique=True)
    business_phone_number = db.Column(db.String(20),nullable=True)
    business_website = db.Column(db.String(150), nullable=True) 
    business_rcnumber = db.Column(db.String(60), nullable=True)
    business_reg_file = db.Column(db.String(100), nullable=True)
    business_tin = db.Column(db.String(60), nullable=True)
    business_tin_file = db.Column(db.String(60), nullable=True)
    business_desc = db.Column(db.Text())
    business_pitch = db.Column(db.Text())
    business_plan = db.Column(db.String(120))
    business_img1 = db.Column(db.String(120))
    # business_img2 = db.Column(db.String(120))
    # business_img3 = db.Column(db.String(120))
    business_userid = db.Column(db.Integer(),db.ForeignKey('b_user.b_user_id'))
    business_datereg = db.Column(db.DateTime(), default=datetime.utcnow())
    business_status_id = db.Column(db.Integer(),db.ForeignKey('business_status.status_id'))
     

    #set relationships
    state_ = db.relationship("State", back_populates="state_data")
    bdeets = db.relationship("B_user", backref="b_userinfo")
    

class B_user(db.Model, UserMixin): 
    b_user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    b_user_fname = db.Column(db.String(20))
    b_user_lname = db.Column(db.String(20))
    b_user_email= db.Column(db.String(20), unique=True)
    b_user_password= db.Column(db.Text(50))
    b_user_pic = db.Column(db.String(120))

    #b_userinfo = db.relationship("Business", backref="bdeets")


class I_user(db.Model, UserMixin): 
    i_user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    i_user_investment  = db.Column(db.Integer(),db.ForeignKey('investor.investor_id'))
    i_user_fname = db.Column(db.String(20))
    i_user_lname = db.Column(db.String(20))
    i_user_email= db.Column(db.String(20), unique=True)
    i_user_password= db.Column(db.Text(50))

class Investor(db.Model): 
    investor_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    investor_investment_id  = db.Column(db.Integer(),db.ForeignKey('investor_investment.investor_investment_id'))
    investor_fname = db.Column(db.String(20))
    investor_lname = db.Column(db.String(20))
    investor_email= db.Column(db.String(20), unique=True)
    investor_phone = db.Column(db.String(30))
    investor_address = db.Column(db.String(100))
    lga_id = db.Column(db.Integer(),db.ForeignKey('lga.lga_id'))
    state_id = db.Column(db.Integer(),db.ForeignKey('state.state_id'))
    investor_password= db.Column(db.Text(50))
    roi_id = db.Column(db.Integer(),db.ForeignKey('roi.roi_id'))

class Donor(db.Model): 
    donor_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    donor_donation_id  = db.Column(db.Integer(),db.ForeignKey('donor_donation.donor_donation_id'))
    donor_fname = db.Column(db.String(20), nullable=False)
    donor_lname = db.Column(db.String(20), nullable=False)
    donor_email= db.Column(db.String(20), unique=False, nullable=False)
    donor_phone = db.Column(db.String(30), nullable=False)
    donor_address = db.Column(db.String(100), nullable=False)
    lga_id = db.Column(db.Integer(),db.ForeignKey('lga.lga_id'))
    state_id = db.Column(db.Integer(),db.ForeignKey('state.state_id'))
    donor_password= db.Column(db.Text(50), nullable=False)


class D_user(db.Model, UserMixin): 
    d_user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    d_user_investment  = db.Column(db.Integer(),db.ForeignKey('donor.donor_id'))
    d_user_fname = db.Column(db.String(20))
    d_user_lname = db.Column(db.String(20))
    d_user_email= db.Column(db.String(20), unique=True)
    d_user_password= db.Column(db.Text(50))

class Donor_donation(db.Model): 
        donor_donation_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        donor_id  = db.Column(db.Integer(),db.ForeignKey('donor.donor_id'))
        business_id = db.Column(db.Integer(),db.ForeignKey('business.business_id'))


class Investment(db.Model): 
        investment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        investor_option_id  = db.Column(db.Integer(),db.ForeignKey('investment_option.investment_option_id'))
        investment_industry = db.Column(db.Integer(),db.ForeignKey('industry.industry_id'))
        investment_amount = db.Column(db.Float(), nullable=False)
        investment_date = db.Column(db.DateTime(), default=datetime.utcnow()) 
        investment_roi_id = db.Column(db.Integer(),db.ForeignKey('roi.roi_id'))


class Donation(db.Model): 
        donation_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        donation_amount = db.Column(db.Float(), nullable=False)
        donation_date = db.Column(db.DateTime(), default=datetime.utcnow()) 


class Investor_investment(db.Model): 
        investor_investment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        investor_id  = db.Column(db.Integer(),db.ForeignKey('investor.investor_id'))
        investment_startdate = db.Column(db.Integer(),db.ForeignKey('industry.industry_id'))
        investment_enddate = db.Column(db.DateTime(), default=datetime.utcnow()) 
        investment_date = db.Column(db.DateTime(), default=datetime.utcnow()) 
        investor_roi_id = db.Column(db.Integer(),db.ForeignKey('roi.roi_id'))

class Investor_disbursement(db.Model): 
        investor_disbursement_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        investor_investment_id  = db.Column(db.Integer(),db.ForeignKey('investor_investment.investor_investment_id'))
        investor_disbursement_amount = db.Column(db.Float(), nullable=False)
        investment_payment_date = db.Column(db.DateTime(), default=datetime.utcnow()) 

class Business_disbursement(db.Model): 
        investor_disbursement_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        business_id  = db.Column(db.Integer(),db.ForeignKey('business.business_id'))
        business_disbursement_amount = db.Column(db.Float(), nullable=False)
        business_payment_date = db.Column(db.DateTime(), default=datetime.utcnow()) 
     
class roi(db.Model): 
        roi_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        investment_id  = db.Column(db.Integer(),db.ForeignKey('investment.investment_id'))
        investment_period = db.Column(db.String(20), nullable=False)
        roi_amount = db.Column(db.DateTime(), default=datetime.utcnow()) 
        roi_date = db.Column(db.DateTime(), default=datetime.utcnow()) 
        
class investment_option(db.Model):
    investment_option_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    investment_option = db.Column(db.String(100), nullable=False)
class payment(db.Model): 
        payment_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        investor_investment_id  = db.Column(db.Integer(),db.ForeignKey('investor_investment.investor_investment_id'))
        amount = db.Column(db.Float(), nullable=False)
        payment_date = db.Column(db.DateTime(), default=datetime.utcnow()) 
        payment_receipt = db.Column(db.String(120),nullable=True)
        payment_status = db.Column(db.String(100), nullable=False)


   
class Business_type(db.Model): 
    type_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=False)


class State(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(100), nullable=False)

    #set relationship
    state_data = db.relationship("Business", back_populates="state_")


class Industry(db.Model): 
    industry_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    industry_name = db.Column(db.String(100), nullable=False)

   
class Business_status(db.Model): 
    status_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    status =db.Column(db.String(100), nullable=False)



class Review(db.Model): 
    review_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    review_text = db.Column(db.Text(), nullable=False)
    review_user = db.Column(db.Integer(),db.ForeignKey('investor.investor_id'))
    review_date = db.Column(db.DateTime(), default=datetime.utcnow())