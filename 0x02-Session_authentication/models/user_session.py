#!/usr/bin/env python3
"""
create a new authentication system,
based on Session ID stored in database
"""
from .base import Base


class UserSession(Base):
    """UserSession"""

    def __init__(self, *args: list, **kwargs: dict):
        """Init Method"""

        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
