#!/usr/bin/env python3
"""Create the class Auth"""
from flask import request
from typing import List, TypeVar
from os import environ


class Auth:
    """Auth Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if not in list - excluded_paths"""
        if path is None or excluded_paths is None:
            return True
        for pth in excluded_paths:
            if path.startswith(pth.rstrip('/*')):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """return the value of the header request Authorization"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""

        if request is None:
            return None

        return request.cookies.get(environ.get('SESSION_NAME'), None)
