from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from Online_Quiz_Platform.app.forms.login_form import LoginForm
from Online_Quiz_Platform.app.models.user import User
from Online_Quiz_Platform.app.forms.register_form import RegistrationForm
from Online_Quiz_Platform.app.extensions import db

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already exists.")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data,
            email=form.email.data,
            role="student"
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))