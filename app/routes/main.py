from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.services.dashboard_service import (
    get_admin_dashboard_data,
    get_student_dashboard_data
)


main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home():

    return render_template("home.html")


@main.route("/dashboard")
@login_required
def dashboard():

    if current_user.is_admin:

        data = get_admin_dashboard_data()

        return render_template(
            "dashboard/admin_dashboard.html",
            **data
        )

    data = get_student_dashboard_data(
        current_user.id
    )

    return render_template(
        "dashboard/student_dashboard.html",
        **data
    )