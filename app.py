import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CSRFProtect(app)

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["flask_login"]
users = db["users"]
users.create_index("email", unique=True)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if "@" not in email or len(email) > 254:
            message = "Enter a valid email address."
        elif not 8 <= len(password) <= 128:
            message = "Use a password between 8 and 128 characters."
        else:
            try:
                users.insert_one({
                    "email": email,
                    "password_hash": generate_password_hash(password)
                })
                message = "Account created! Your account is saved."
            except DuplicateKeyError:
                message = "An account with this email already exists."

    return render_template("register.html", message=message)