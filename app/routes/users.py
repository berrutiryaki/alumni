"""
User web routes — HTML responses.
Blueprint prefix: /users
Delegates to: UserController
"""

from flask import Blueprint
from app.controllers.user_controller import UserController

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET"])
def index():
    """List all users (HTML)."""
    result = UserController.index()
    rows = "".join(
        f"<tr><td>{u['id']}</td><td>{u['name']}</td><td>{u['email']}</td>"
        f"<td>{u['department']}</td><td>{u['graduation_year']}</td></tr>"
        for u in result["users"]
    )
    return f"""
    <h1>Users</h1>
    <table border='1'>
      <tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>Graduation Year</th></tr>
      {rows or '<tr><td colspan=5>No users yet.</td></tr>'}
    </table>
    """, 200, {"Content-Type": "text/html"}


@users_bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    """Show a single user (HTML)."""
    result = UserController.show(user_id)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404, {"Content-Type": "text/html"}
    u = result["user"]
    return f"""
    <h1>User #{u['id']}</h1>
    <p><b>Name:</b> {u['name']}</p>
    <p><b>Email:</b> {u['email']}</p>
    <p><b>Department:</b> {u['department']}</p>
    <p><b>Graduation Year:</b> {u['graduation_year']}</p>
    """, 200, {"Content-Type": "text/html"}


@users_bp.route("/", methods=["POST"])
def create():
    """Create a new user (HTML form submission)."""
    from flask import request
    data = request.form.to_dict()
    result = UserController.create(data)
    if not result["success"]:
        return f"<h2>400 — {result['error']}</h2>", 400, {"Content-Type": "text/html"}
    u = result["user"]
    return f"<h2>User #{u['id']} ({u['name']}) created.</h2>", 201, {"Content-Type": "text/html"}


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update(user_id):
    """Fully replace a user (HTML form submission)."""
    from flask import request
    data = request.form.to_dict()
    result = UserController.update(user_id, data)
    if not result["success"]:
        status = 404 if "not found" in result["error"] else 400
        return f"<h2>{status} — {result['error']}</h2>", status, {"Content-Type": "text/html"}
    u = result["user"]
    return f"<h2>User #{u['id']} updated.</h2>", 200, {"Content-Type": "text/html"}


@users_bp.route("/<int:user_id>", methods=["PATCH"])
def partial_update(user_id):
    """Partially update a user (HTML form submission)."""
    from flask import request
    data = request.form.to_dict()
    result = UserController.partial_update(user_id, data)
    if not result["success"]:
        return f"<h2>404 — {result['error']}</h2>", 404, {"Content-Type": "text/html"}
    u = result["user"]
    return f"<h2>User #{u['id']} partially updated.</h2>", 200, {"Content-Type": "text/html"}


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    """Delete a user (HTML)."""
    result = UserController.delete(user_id)
    if not result["success"]:
        return f"<h2>404 — {result['message']}</h2>", 404, {"Content-Type": "text/html"}
    return f"<h2>{result['message']}</h2>", 200, {"Content-Type": "text/html"}
