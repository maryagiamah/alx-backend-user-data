#!/usr/bin/env python3
"""Create a class SessionAuth that inherits from Auth
"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""

        if not isinstance(user_id, str):
            return None

        ses_id = str(uuid.uuid4())
        self.user_id_by_session_id[ses_id] = user_id

        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""

        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        (overload) that returns a User instance
        based on a cookie value
        """

        if request is None:
            return None

        ses_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(ses_id)

        print(user_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""

        if request is None:
            return False

        ses_id = self.session_cookie(request)

        if ses_id:
            if self.user_id_for_session_id(ses_id):
                del self.user_id_by_session_id[ses_id]
                return True
        return False
