from datetime import datetime
from fundsapp import db
from sqlalchemy import ForeignKey

class Business(db.Model):
    business_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    business_name = db.Column(db.String(100), nullable = False)
    business_email = db.Column(db.String(120), nullable = False)
    business_password = db.Column(db.String(200), nullable = True)
    business_phone = db.Column(db.String(120), nullable = True)
    business_address = db.Column(db.String(255), nullable = True)
    business_type = db.Column(db.String(120), nullable = True)
    business_story = db.Column(db.Text(120), nullable = True)
    business_websiteurl = db.Column(db.String(120), nullable = True)
    business_rcnumber = db.Column(db.String(120), nullable = True)
    business_profile_pic = db.Column(db.String(120), nullable = True)
    business_pic_one = db.Column(db.String(120), nullable = True)
    business_pic_two = db.Column(db.String(120), nullable = True)
    business_pic_three = db.Column(db.String(120), nullable = True)
    business_entry_status = db.Column(db.String(120), nullable = True)
     
    # RELATIONSHIPS
    industry = db.relationship("Industry", back_populates="business_data")
    business_disbursement = db.relationship("Business_disbursement", back_populates="business_data")
    donation = db.relationship("Donation", back_populates="business_data")
    industry = db.relationship("Industry", back_populates="business_data")
    payment = db.relationship("Payment", back_populates="business_data")
    
    
class Business_owner(db.Model):
    __tablename__ = "entrepreneur"
    entrepreneur_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    entrepreneur_name = db.Column(db.String(100), nullable = False)
    entrepreneur_email = db.Column(db.String(120), nullable = False)
    entrepreneur_password = db.Column(db.String(200), nullable = True)
    entrepreneur_phone = db.Column(db.String(120), nullable = True) 
        
         # RELATIONSHIPS
    business_data = db.relationship("Business", back_populates="entrepreneurs")
    investment = db.relationship("Investment", back_populates="entrepreneurs")
    business_disbursement = db.relationship("Business_disbursement", back_populates="entrepreneurs")
    administrator = db.relationship("Admin", back_populates="entrepreneurs")
    
    
class BusinessDisbursement(db.Model):
    business_disbursementid = db.Column(db.Integer, autoincrement = True, primary_key = True)
    business_disbursement_amt = db.Column(db.Float(), nullable = False)
    business_disbursement_date = db.Column(db.DateTime(), default=datetime.utcnow)
    
    # RELATIONSHIPS
    business = db.relationship("Business", back_populates="b_disburse")
    payment = db.relationship("Payment", back_populates="b_disburse")
    
    

class Donation(db.Model):
    donation_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    donation_amt = db.Column(db.Float(), nullable = False)
    donation_date = db.Column(db.DateTime(), default=datetime.utcnow)
    
    # RELATIONSHIPS
    business = db.relationship("Business", back_populates="donation_data")
    donor = db.relationship("Donor", back_populates="donation_data")
    
        
class Donor(db.Model):
    donor_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    donor_name = db.Column(db.String(100), nullable = False)
    donor_email = db.Column(db.String(120), nullable = False)
    donor_password = db.Column(db.String(200), nullable = True)
    donor_phone = db.Column(db.String(120), nullable = True)
    
     # RELATIONSHIPS
    business = db.relationship("Business", back_populates="donors")
    donation = db.relationship("Donation", back_populates="donors")
    
    
class Industry(db.Model):
    industry_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    industry_type = db.Column(db.String(120), nullable = True)
    
     # RELATIONSHIPS
    business = db.relationship("Business", back_populates="industry_data")
    
    
    
class Investment(db.Model):
    investment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    
         # RELATIONSHIPS
    investor_investment = db.relationship("", back_populates="")
    payment = db.relationship("Payment", back_populates="payment_data")
    roi = db.relationship("Roi", back_populates="payment_data")
    
    
    

class Investor(db.Model):
    investor_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    investor_name = db.Column(db.String(100), nullable = False)
    investor_email = db.Column(db.String(120), nullable = False)
    investor_password = db.Column(db.String(200), nullable = True)
    investor_phone = db.Column(db.String(120), nullable = True) 
        
         # RELATIONSHIPS
    roi = db.relationship("Roi", back_populates="investors")
    investment = db.relationship("Investment", back_populates="investors")
    investor_disbursement = db.relationship("Investor_Disbursement", back_populates="investors")
    payment = db.relationship("Payment", back_populates="investors")
    
    
    
class Investor_investment(db.Model):
    investor_id = db.Column(db.Integer, ForeignKey('investor.investor_id'), primary_key = True, autoincrement=False)
    investment_id = db.Column(db.Integer, db.ForeignKey('investment.investment_id'),nullable=False)  
    start_date = db.Column(db.DateTime(), default=datetime.utcnow)
    end_date = db.Column(db.DateTime(), default=datetime.utcnow)
        
         # RELATIONSHIPS
    investor = db.relationship("Investor", back_populates = "investor_investment_data")  
    investment = db.relationship("Investment", back_populates = "investor_investment_data")
    roi = db.relationship("Roi", back_populates = "investor_investment_data")
    
      
class Investor_disbursement(db.Model):
    investor_disbursement_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    investor_disbursement_amt = db.Column(db.Float(), nullable = False)
    investor_disbursement_date = db.Column(db.DateTime(), default=datetime.utcnow)
            
         # RELATIONSHIPS
    investor_investment = db.relationship("Investor_investment", back_populates="i_disburse")
    investor = db.relationship("Investor", back_populates="i_disburse")
    payment = db.relationship("Payment", back_populates="i_disburse")
    roi = db.relationship("Roi", back_populates="i_disburse")
    
    
class Payment(db.Model):
    payment_id = db.Column(db.Integer, autoincrement =True, primary_key = True)
    amount = db.Column(db.Float(), nullable = False)
    payment_receipt = db.Column(db.String(120), nullable = False)
    payment_status =  db.Column(db.String(120), nullable = True) 
                
         # RELATIONSHIPS
    investment = db.relationship("Investment", back_populates="payment_data")
    business = db.relationship("Business", back_populates="payment_data")
    business_disbursement = db.relationship("Business_disbursement", back_populates="payment_data")
    investor_disbursement = db.relationship("Investor_disbursement", back_populates="payment_data")
    administrator = db.relationship("Admin", back_populates="payment_data")
    
    
    
class Roi():
    roi_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    investment_period = db.Column(db.String(120), nullable = False)
    investor_investment_period = db.Column(db.Float(), default=datetime.utcnow)
    investor_disbursement_date = db.Column(db.DateTime(), default=datetime.utcnow)
            
         # RELATIONSHIPS
    investment = db.relationship("Investment", back_populates="roi_data")
    investor_investment = db.relationship("Investor_investment", back_populates="roi_data")
    investor_disbursement = db.relationship("Investor_disbursement", back_populates="roi_data")
    
    

'''class Review(db.Model):
    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review_msg = db.Column(db.Text(),nullable=False)
    review_date =db.Column(db.DateTime(), default=datetime.utcnow)
    review_id = db.Column(db.Integer, db.ForeignKey('investor.investor_id'),nullable=False)    
    
    # RELATIONSHIPS
    investors = db.relationship("Investor", back_populates = "i_review")
    administrator = db.relationship("Admin", back_populates = "i_review")
    all_comments = db.relationship("Comments", back_populates="i_review")
    
    

class Contact(db.Model):
    contact_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    contact_title = db.Column(db.String(120), nullable = False)
    contact_msg = db.Column(db.String(255), nullable = False)
    contact_date =db.Column(db.DateTime(), default=datetime.utcnow)
    contact_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),nullable=False)  
    contact_topicid =db.Column(db.Integer, db.ForeignKey('topics.topic_id'),nullable=False)  
    
    # RELATIONSHIPS
    i_user = db.relationship("Investment_user", back_populates="contact_support")
    b_user = db.relationship("Business_user", back_populates="contact_support")
    
    
#  --iNVESTORS' REVIEW/FEEDBACK-- 
class Investment_user(db.Model):  
    i_user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    i_user_fullname = db.Column(db.String(100),nullable=False)
    i_user_email = db.Column(db.String(120)) 
    i_user_pwd=db.Column(db.String(120),nullable=True)
    i_user_phone=db.Column(db.String(120),nullable=True) 
    i_user_pix=db.Column(db.String(120),nullable=True) 
    i_user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)
    
    # FOREIGN KEY 
    i_user_business_id=db.Column(db.Integer, db.ForeignKey('investor.investor_name'))  
    
    
    # RELATIONSHIPS
    business_data = db.relationship("Business", back_populates="i_user")
    contact_support = db.relationship("Contact", back_populates="i_user")
    admin = db.relationship("Topics", back_populates="i_user")
    investor = db.relationship("Investor", back_populates="i_user")
    
    
#  --SUPPORT FOR BOTH iNVESTORS AND BUSINESSES'-- 
class business_user(db.Model):  
    b_user_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    b_user_fullname = db.Column(db.String(100),nullable=False)
    b_user_email = db.Column(db.String(120)) 
    b_user_pwd=db.Column(db.String(120),nullable=True)
    b_user_phone=db.Column(db.String(120),nullable=True) 
    b_user_pix=db.Column(db.String(120),nullable=True) 
    b_user_datereg=db.Column(db.DateTime(), default=datetime.utcnow)
    
    # FOREIGN KEY 
    b_user_business_id=db.Column(db.Integer, db.ForeignKey('business.business_name'))  
    
    
    # RELATIONSHIPS
    business_data = db.relationship("Business", back_populates="business_user_data")
    administrator = db.relationship("Admin", back_populates="business_user_data")
    contact_support = db.relationship("Contact", back_populates="business_user_data")'''
 

class Admin(db.Model):
    admin_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)
     
     
    # RELATIONSHIPS
    i_user = db.relationship("Investment_user", back_populates="administrator")
    b_user = db.relationship("Business_user", back_populates="administrator")
    payment_data = db.relationship("Payment", back_populates="administrator")
    entrepreneurs = db.relationship("Entrepreneur", back_populates = "entrepreneurs")
    