from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data.strip()
        password = login_form.password.data

        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'

        if error is None:
            login_user(user)

            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.scalar(db.select(User).where(User.name == form.user_name.data)):
            flash("That username is already taken.")
            return render_template('user.html', form=form, heading='Register')

        if db.session.scalar(db.select(User).where(User.email == form.email.data)):
            flash("That email is already registered.")
            return render_template('user.html', form=form, heading='Register')

        user = User(
            name=form.user_name.data.strip(),
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.strip(),
            phone=(form.phone.data.strip() if form.phone.data else None),
            street_address=(form.street_address.data.strip() if form.street_address.data else None),
            password_hash=generate_password_hash(form.password.data).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.")
        return redirect(url_for('auth.login'))

    return render_template('user.html', form=form, heading='Register')