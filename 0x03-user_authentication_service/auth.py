#!/usr/bin/env python3
"""Auth"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password"""

    return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers user"""

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                    email,
                    _hash_password(password)
                )
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """check user password"""

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """returns a session ID as str"""

        try:
            user = self._db.find_user_by(email=email)
            updates = {"session_id": _generate_uuid()}

            self._db.update_user(user.id, **updates)
            return updates['session_id']
        except NoResultFound:
            pass
