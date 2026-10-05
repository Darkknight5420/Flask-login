import os
from flask import Flask, render_template, session, redirect
import pymongo


app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

#Routed
from user import routes


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard/")
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)