"""
User web routes — HTML responses.
Blueprint prefix: /users
Delegates to: UserController
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.user_controller import UserController

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"])
def index():
    """List all users (HTML)."""
    result = UserController.index()
    return render_template("user/index.html", users=result["users"])


@users_bp.route("/new", methods=["GET"])
def new():
    """Show the form to create a new user."""
    return render_template("user/create.html", error=None)


@users_bp.route("/", methods=["POST"])
def create():
    """Process the form submission and create a new user."""
    data = request.form.to_dict()
    result = UserController.create(data)
    
    if not result["success"]:
        # Re-render the form with the error message
        return render_template("user/create.html", error=result["error"]), 400
        
    # On success, redirect back to the user list
    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>/edit", methods=["GET"])
def edit(user_id):
    """Show the form to edit an existing user."""
    result = UserController.show(user_id)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404
    return render_template("user/edit.html", user=result["user"], error=None)


@users_bp.route("/<int:user_id>/edit", methods=["POST"])
def update(user_id):
    """Process the edit form submission."""
    data = request.form.to_dict()
    result = UserController.update(user_id, data)
    
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        if status == 400:
            # Re-render form with errors
            user_result = UserController.show(user_id)
            user_data = user_result["user"] if user_result["success"] else data
            return render_template("user/edit.html", user=user_data, error=result["error"]), 400
        return f"<h2>{status} — {result['error']}</h2>", status
        
    return redirect(url_for("users.index"))


@users_bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    """Process the delete form submission."""
    result = UserController.delete(user_id)
    if not result["success"]:
        return f"<h2>404 — {result['message']}</h2>", 404
    return redirect(url_for("users.index"))
