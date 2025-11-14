import json
import os

from appdirs import user_data_dir


class CredentialStore:
    def __init__(self, app_name="ResolveKitsuTool"):
        self.data_dir = user_data_dir(app_name)
        os.makedirs(self.data_dir, exist_ok=True)
        self.path = os.path.join(self.data_dir, "session.json")

    def save_session(self, session_data: dict):
        with open(self.path, "w") as f:
            json.dump(session_data, f)

    def load_session(self) -> dict | None:
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            return json.load(f)

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)
