#!/usr/bin/env python3
from models.user_session import UserSession

UserSession.load_from_file()
print(UserSession.search({'session_id': "44039914-d22d-435d-a613-030de68d371b"})[0].user_id)
