#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def home():
    """Return welcome page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def add_user():
    """Add user from post data"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify(
                {"email": email, "message": "user created"}
            )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def create_session():
    """create user_session"""

    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', AUTH.create_session(email))
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
