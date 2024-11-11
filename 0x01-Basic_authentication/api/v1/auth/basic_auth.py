#!/usr/bin/env python3
"""Basic Auth"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth Class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of
        the Authorization header
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.partition('Basic ')[2]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            val = base64.b64decode(base64_authorization_header)
            return val.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password
        from the Base64 decoded value
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if not decoded_base64_authorization_header.find(':'):
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on
        his email and password
        """
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        try:
            auth_header = self.authorization_header(request)
            extract_base64 = self.extract_base64_authorization_header(
                    auth_header
                )
            decode_val = self.decode_base64_authorization_header(
                    extract_base64
                )
            user_email, user_pwd = self.extract_user_credentials(decode_val)
            return self.user_object_from_credentials(user_email, user_pwd)
        except Exception:
            pass
