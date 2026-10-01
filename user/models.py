from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

    def signup(self):
        print(request.form)

        user ={
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if db.users.find_one({"email": user['email'] }):
            return jsonify({"error": "Email adress already in use"}), 400

        if db.users.insert_one(user):
            return jsonify(user), 200

        return jsonify({"error": "signup failed" }), 400