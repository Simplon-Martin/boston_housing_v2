"""Routes for user authentication."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import current_user, login_user, login_required, logout_user

from app.models import User
from app.db import db

# Blueprint Configuration
auth = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


@auth.route("/signup")
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    print(email)
    print(name)
    print(password)

    user = User.User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # ct stores current time
    ct = datetime.datetime.now()

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User.User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                         created_on=ct, last_login=None)


    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # ct stores current time
    ct = datetime.datetime.now()

    user.last_login = ct

    db.session.commit()

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
