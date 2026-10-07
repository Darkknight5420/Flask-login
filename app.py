import os

import pymongo
from flask import Flask, render_template, session, redirect

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "FLASK_SECRET_KEY is missing. "
        "Set it in the terminal before starting Flask."
    )

client = pymongo.MongoClient(
    "mongodb://127.0.0.1:27017/",
    serverSelectionTimeoutMS=5000
)

db = client.user_login_system

from user import routes


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard/")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)