from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField, SelectField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, Email
from fundsapp.models import B_user, I_user




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
        b_user = B_user.query.filter_by(b_user_email = email.data).first()
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
    
    btype = SelectField("btype",
            validators=[
            DataRequired()]),

    b_industry = SelectField("b_industry",
        validators=[
            DataRequired()]),       

    regnumber = StringField("regnumber",
    validators=[
         DataRequired(),
         Regexp(
            "^[A-Za-z] [A-Za-a0-9.]*", 0, "Please provide a valid number"
            ),
        ],
            render_kw={"placeholder": "Enter your BN or RC number"})

    # regfile = FileField("regfile",
    #         validators=[
    #         FileRequired(), FileAllowed(["jpg", "jpeg", "png", "doc", "docx", "pdf"], "File not allowed!")])

    tin = StringField("tin",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid number")],
            render_kw={"placeholder": "Enter your tax number"})

    
    # taxfile = FileField("taxfile",
    #         validators=[
    #         FileRequired(), FileAllowed(["jpg", "jpeg", "png", "doc", "docx", "pdf"], "File not allowed!")])
    
    b_desc = TextAreaField("b_desc",
         validators=[
            DataRequired(),
            length(min=1, max=800)])
    
    pitch = StringField("pitch",
        validators=[
            DataRequired(),
            length(min=1, max=800)])

    # planfile = FileField("planfile",
    #     validators=[
    #         DataRequired(), FileAllowed(["txt", "doc", "docx", "pdf"], "File not allowed!")])
    
    # img1 = FileField("img1",
    #     validators=[
    #         FileRequired(), FileAllowed(["jpg", "png", "jpeg", "JPEG"], "Images only!"),
    #         length(min=2, max=20)])
    
    # img2 = FileField("img2",
    #     validators=[
    #         FileRequired(), FileAllowed(["jpg", "png", "jpeg", "JPEG"], "Images only!")])
    
    
    # img3 = FileField("img3",
    #     validators=[
    #         DataRequired(), FileAllowed(["jpg", "png", "jpeg", "JPEG"], "Imaages only!")])

    submit = SubmitField("Submit")
    
    def validate_email(self, email):
        b_user =B_user.query.filter_by(b_user_email = email.data).first()
        if b_user:
            raise ValidationError("That email already have an account. Please choose a different one.")  



class DonorSignupForm(FlaskForm):
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
        d_user =I_user.query.filter_by(i_user_email = email.data).first()
        if d_user:
            raise ValidationError("That email already have an account. Please choose a different one.")



class DonorLoginForm(FlaskForm):
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
    


#  --  VALIDATION CLASSES  --  THESE ARE THE CLASSES FOR IUSER VALIDATION

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
        i_user =I_user.query.filter_by(i_user_email = email.data).first()
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

