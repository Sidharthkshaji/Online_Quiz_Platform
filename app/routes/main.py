from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/dashboard")
@login_required
def dashboard():

    if current_user.is_admin:
        return render_template("dashboard/admin_dashboard.html")

    return render_template("dashboard/dashboard.html")