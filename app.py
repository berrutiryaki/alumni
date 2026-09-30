from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

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
        "version": "1.0.0",
    }
}

Swagger(app, config=swagger_config, template=swagger_template)


@app.route("/")
def index():
    return """
<h1>Alumni Platform</h1>
<p>Welcome to Alumni tracking portal.</p>
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


users = []


@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Get all users.
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            users:
              type: array
              items:
                type: object
    """
    return jsonify({"status": "success", "users": users}), 200


@app.route("/api/users", methods=["POST"])
def create_user():
    """
    Create a new user.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Full name of the user
      - name: email
        in: formData
        type: string
        required: true
        description: Email address
      - name: department
        in: formData
        type: string
        description: Academic department
      - name: graduation_year
        in: formData
        type: integer
        description: Year of graduation
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            user:
              type: object
    """
    data = request.form.to_dict() if request.form else request.get_json() or {}
    user = {"id": len(users) + 1, **data}
    users.append(user)
    return jsonify({"status": "success", "user": user}), 201


@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):
    """
    Get a user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            user:
              type: object
      404:
        description: User not found
    """
    user = next((u for u in users if u["id"] == id), None)
    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 404
    return jsonify({"status": "success", "user": user}), 200


@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):
    """
    Fully replace a user by ID.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: User ID
      - name: name
        in: formData
        type: string
      - name: email
        in: formData
        type: string
      - name: department
        in: formData
        type: string
      - name: graduation_year
        in: formData
        type: integer
    responses:
      200:
        description: User replaced successfully
      404:
        description: User not found
    """
    user = next((u for u in users if u["id"] == id), None)
    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 404
    data = request.form.to_dict() if request.form else request.get_json() or {}
    user.clear()
    user.update({"id": id, **data})
    return jsonify({"status": "success", "user": user}), 200


@app.route("/api/users/<int:id>", methods=["PATCH"])
def partial_update_user(id):
    """
    Partially update a user by ID.
    ---
    tags:
      - Users
    consumes:
      - multipart/form-data
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: User ID
      - name: name
        in: formData
        type: string
      - name: email
        in: formData
        type: string
      - name: department
        in: formData
        type: string
      - name: graduation_year
        in: formData
        type: integer
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
    """
    user = next((u for u in users if u["id"] == id), None)
    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 404
    data = request.form.to_dict() if request.form else request.get_json() or {}
    user.update(data)
    return jsonify({"status": "success", "user": user}), 200


@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    """
    Delete a user by ID.
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = next((u for u in users if u["id"] == id), None)
    if user is None:
        return jsonify({"status": "error", "message": "User not found"}), 404
    users.remove(user)
    return jsonify({"status": "success", "message": f"User {id} deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
