import json
import os

from appdirs import user_data_dir


class CredentialStore:
    def __init__(self, appName="ResolveKitsuTool"):
        self.dataDir = user_data_dir(appName)
        os.makedirs(self.dataDir, exist_ok=True)
        self.path = os.path.join(self.dataDir, "session.json")

    def saveSession(self, sessionData: dict):
        with open(self.path, "w") as f:
            json.dump(sessionData, f)

    def loadSession(self) -> dict | None:
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            return json.load(f)

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)
