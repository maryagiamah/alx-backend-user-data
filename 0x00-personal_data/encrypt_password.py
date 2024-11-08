#!/usr/bin/env python3
"""Use the bcrypt package to perform the hashing"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    byte_pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte_pwd, salt)
