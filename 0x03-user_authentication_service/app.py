#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from typing import Any, Tuple

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def home():
    """Return welcome page"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
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
def login():
    """create user_session"""

    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', AUTH.create_session(email))
    return res


@app.route("/sessions", methods=['DELETE'])
def logout():
    """destroy the session and redirect the user to GET """

    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for(home))


@app.route("/profile", methods=['GET'])
def profile():
    """Use it to find the user"""

    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """generate a new token"""

    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """Update the password"""

    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
