#!/usr/bin/env python3
"""inherits from SessionExpAuth"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth"""

    def create_session(self, user_id=None):
        """stores new instance of UserSession"""

        ses_id = super().create_session(user_id)

        if ses_id is None:
            return None

        user = UserSession(**{"user_id": user_id, "session_id": ses_id})
        user.save()

        return ses_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession"""

        try:
            users = UserSession.search({"session_id": session_id})
            if users[0].created_at:

                if self.session_duration <= 0:
                    return users[0].user_id

                exp_time = users[0].created_at + timedelta(
                        seconds=self.session_duration
                    )

                if datetime.utcnow() < exp_time:
                    return users[0].user_id
            return None
        except Exception:
            return None

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID"""

        try:
            session_id = self.session_cookie(request)
            users = UserSession.search({"session_id": session_id})

            if users[0].user_id:
                users[0].remove()
                return True
            return False
        except Exception:
            return False
