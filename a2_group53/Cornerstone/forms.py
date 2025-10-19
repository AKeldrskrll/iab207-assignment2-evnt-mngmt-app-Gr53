from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateField, SelectField, FloatField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Email, EqualTo, Optional

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    #fname lname
    first_name=StringField("First Name", validators=[InputRequired(), Length(max=80)])
    last_name=StringField("Last Name", validators=[InputRequired(), Length(max=80)])

    user_name=StringField("User Name", validators=[InputRequired(), Length(min=3, max=80)])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to confirm
    password=PasswordField("Password", validators=[
                InputRequired(), Length(min=6), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #additional fields
    phone = StringField("Contact Number", validators=[Length(max=40)])
    street_address = StringField("Street Address", validators=[Length(max=200)])

    # submit button
    submit = SubmitField("Register")

class EventForm(FlaskForm):
    title = StringField("Event title", validators=[InputRequired(), Length(max=120)])
    artist = StringField("Artist", validators=[InputRequired(), Length(max=120)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(max=500)])
    date = DateField("Date", validators=[InputRequired()], format="%Y-%m-%d")
    venue = StringField("Venue", validators=[InputRequired(), Length(max=120)])
    category = SelectField("Genre", choices=[("Rap","Rap"), ("Soul","Soul"), ("Jazz","Jazz"), ("RnB","RnB")], validators=[InputRequired()])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
    capacity = IntegerField("Capacity", validators=[InputRequired(), NumberRange(min=0)])
    price = FloatField("Ticket Price", validators=[InputRequired(), NumberRange(min=0)], render_kw={"step": "0.01"})
    submit = SubmitField("Post Event")

class CommnetForm(FlaskForm):
    body = TextAreaField("Add a comment", validators=[InputRequired(), Length(min=1, max=1000)])
    submit = SubmitField("Post")

class OrderForm(FlaskForm):
    qty = IntegerField("Number of tickets", validators=[InputRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField("Buy Tickets")
