#!/usr/bin/env python3
"""Create a class SessionExpAuth that inherits from SessionAuth"""
from os import environ
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth"""

    def __init__(self):
        """Init Method"""
        try:
            ses_dur = environ.get('SESSION_DURATION')
            self.session_duration = int(ses_dur)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID by calling super()"""
        ses_id = super().create_session(user_id)

        if ses_id is None:
            return None

        self.user_id_by_session_id[ses_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }

        return ses_id

    def user_id_for_session_id(self, session_id=None):
        """return user_id from the session dictionary"""

        try:
            user_id = self.user_id_by_session_id.get(session_id)["user_id"]

            ses_dict = self.user_id_by_session_id.get(session_id)
            if self.session_duration <= 0:
                return user_id
            if 'created_at' in ses_dict:
                exp_time = ses_dict['created_at'] + timedelta(
                        seconds=self.session_duration
                    )
                if datetime.now() < exp_time:
                    return user_id
            return None
        except Exception:
            return None
