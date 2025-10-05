from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired(), Length(min=3, max=80)])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[
                InputRequired(), Length(min=6), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #additional fields
    phone = StringField("Contact Number", validators=[Length(max=40)])
    street_address = StringField("Street Address", validators=[Length(max=200)])

    # submit button
    submit = SubmitField("Register")