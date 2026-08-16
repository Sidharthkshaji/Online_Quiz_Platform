from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.forms.login_form import LoginForm
from app.forms.register_form import RegistrationForm
from app.models.user import User
from app.extensions import db

import re
import secrets


auth = Blueprint(
    "auth",
    __name__
)


def generate_unique_username(name):
    """
    Generate a random username based on the user's name.

    Example:
        Sidharth K Shaji
        -> sidharthkshaji_4827
    """

    clean_name = re.sub(
        r"[^a-zA-Z0-9]",
        "",
        name
    ).lower()

    if not clean_name:
        clean_name = "user"

    base = clean_name[:35]

    while True:

        random_number = secrets.randbelow(
            9000
        ) + 1000

        username = f"{base}_{random_number}"

        exists = User.query.filter_by(
            username=username
        ).first()

        if not exists:
            return username


@auth.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.home")
        )

    form = RegistrationForm()

    if form.validate_on_submit():

        generated_username = (
            generate_unique_username(
                form.name.data
            )
        )

        user = User(
            name=form.name.data.strip(),
            username=generated_username,
            email=form.email.data.strip().lower(),
            role="student"
        )

        user.set_password(
            form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash(
            f"Account created successfully. "
            f"Your username is @{generated_username}.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/register.html",
        form=form
    )


@auth.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.home")
        )

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data.strip().lower()
        ).first()

        if user and user.check_password(
            form.password.data
        ):

            login_user(user)

            flash(
                f"Welcome back, {user.name}!",
                "success"
            )

            return redirect(
                url_for("main.home")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "auth/login.html",
        form=form
    )


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )