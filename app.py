from flask import Flask

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
