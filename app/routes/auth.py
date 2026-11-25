"""
Authentication & Registration web routes — HTML responses.
Routes:
  - GET  /register — Render registration form (register.html)
  - POST /register — Validate inputs, hash password, create user, auto-login & redirect to /
  - GET  /login    — Render login form (login.html)
  - POST /login    — Authenticate user, set session['user_id'] & redirect to /
  - POST /logout   — Clear session & redirect to /
"""

from flask import Blueprint, redirect, render_template, request, session, url_for
from app.controllers.user_controller import UserController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET"])
def register_form():
    """Render the user registration page."""
    return render_template("register.html", error=None, form_data={})


@auth_bp.route("/register", methods=["POST"])
def register_submit():
    """Process the registration form submission, clear old session, auto-login, and redirect to homepage."""
    data = request.form.to_dict()
    result = UserController.register(data)

    if not result["success"]:
        return render_template("register.html", error=result["error"], form_data=data), 400

    session.clear()
    session["user_id"] = result["user"]["id"]
    return redirect(url_for("index"))


@auth_bp.route("/login", methods=["GET"])
def login_form():
    """Render the user login page."""
    return render_template("login.html", error=None, form_data={})


@auth_bp.route("/login", methods=["POST"])
def login_submit():
    """Authenticate user credentials, clear old session, start fresh session, and redirect to homepage."""
    data = request.form.to_dict()
    result = UserController.login(data)

    if not result["success"]:
        return render_template("login.html", error=result["error"], form_data=data), 401

    session.clear()
    session["user_id"] = result["user"]["id"]
    return redirect(url_for("index"))


@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    """Clear the active user session and redirect to homepage."""
    session.clear()
    return redirect(url_for("index"))
