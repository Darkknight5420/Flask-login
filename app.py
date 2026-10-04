from flask import Flask, render_template, session, redirect 
from functools import wraps
import pymongo


app = Flask(__name__)
app.secret_key= "b'6\n\xd5\x0e\xb9\x18\xcfP\xe3\xeaM\xc4r[\xc9H"

client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system


# Decorators
def login_reuired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')
        return wrap  

#Routed
from user import routes


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

    