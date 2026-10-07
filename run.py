import os
from flask import Flask, jsonify
from flasgger import Swagger

from app.routes.users import users_bp
from app.routes.api_users import api_users_bp

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates'))

# ------------------------------------------------------------------
# Swagger / OpenAPI
# ------------------------------------------------------------------

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/api/swagger.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/swagger",
}

swagger_template = {
    "info": {
        "title": "Alumni API",
        "description": "Alumni Tracking & Networking Platform REST API",
        "version": "1.1.0",
    },
    "tags": [
        {"name": "Health", "description": "API status"},
        {"name": "Users", "description": "User CRUD via ApiUserController"},
    ],
}

Swagger(app, config=swagger_config, template=swagger_template)

# ------------------------------------------------------------------
# Blueprints
# ------------------------------------------------------------------

app.register_blueprint(users_bp)       # /users  — HTML (UserController)
app.register_blueprint(api_users_bp)   # /api/users — JSON (ApiUserController)

# ------------------------------------------------------------------
# General routes
# ------------------------------------------------------------------


@app.route("/")
def index():
    return """
<h1>Alumni Platform</h1>
<p>Welcome to Alumni tracking portal.</p>
<ul>
  <li><a href="/users">Users (HTML)</a></li>
  <li><a href="/api/users/">API Users (JSON)</a></li>
  <li><a href="/api/swagger">Swagger Docs</a></li>
</ul>
""", 200, {"Content-Type": "text/html"}


@app.route("/about")
def about():
    return """
<h1>About</h1>
<p>Alumni is a tracking and networking platform connecting graduates, students, and institutions.</p>
""", 200, {"Content-Type": "text/html"}


@app.route("/hello")
def hello():
    return "Hello, World!", 200, {"Content-Type": "text/plain"}


@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello, {name.capitalize()}!", 200, {"Content-Type": "text/plain"}


@app.route("/sum/<int:number1>/<int:number2>")
def sum_numbers(number1, number2):
    return str(number1 + number2), 200, {"Content-Type": "text/plain"}


# ------------------------------------------------------------------
# Health check
# ------------------------------------------------------------------


@app.route("/api/health")
def health():
    """
    Health check endpoint.
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            message:
              type: string
              example: healthy
    """
    return jsonify({"status": "ok", "message": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
