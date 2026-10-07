import uuid

from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db


class User:
    def start_session(self, user):
        session.clear()

        session["logged_in"] = True
        session["user"] = {
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }

        return jsonify(session["user"]), 200

    def signup(self):
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return jsonify({
                "error": "Please fill in all fields."
            }), 400

        if db.users.find_one({"email": email}):
            return jsonify({
                "error": "Email address already in use."
            }), 400

        user = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "email": email,
            "password": pbkdf2_sha256.hash(password)
        }

        db.users.insert_one(user)

        # Signup creates the account without logging the user in.
        session.clear()

        return jsonify({
            "message": (
                f"Congratulations {name}, "
                "you have successfully signed up! "
                "Please log in with your email and password."
            ),
            "email": email
        }), 201

    def signout(self):
        session.clear()
        return redirect("/")

    def login(self):
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return jsonify({
                "error": "Please enter your email and password."
            }), 400

        user = db.users.find_one({"email": email})

        if user and pbkdf2_sha256.verify(password, user["password"]):
            return self.start_session(user)

        return jsonify({
            "error": "Invalid email or password."
        }), 401