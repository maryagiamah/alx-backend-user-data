#!/usr/bin/env python3
"""
Create a new Flask view that handles all routes for the Session authentication
"""
from api.v1.views import sess_views
from flask import abort, jsonify, request
from models.user import User
from os import environ


@sess_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Login Method"""

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search(attributes={'email': email})

    if users == []:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            sess_id = auth.create_session(user.id)
            res = jsonify(user.to_json())
            res.set_cookie(environ.get('SESSION_NAME'), sess_id)
            return res
    return jsonify({"error": "wrong password"}), 401
