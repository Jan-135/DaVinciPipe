import json
import os

from appdirs import user_data_dir


class ConfigStore:
    def __init__(self, appName="ResolveKitsuTool"):
        self.dataDir = user_data_dir(appName)
        os.makedirs(self.dataDir, exist_ok=True)
        self.path = os.path.join(self.dataDir, "config_path.json")

    def saveConfigPath(self, configPath: str):
        with open(self.path, "w") as f:
            json.dump({"config_path": configPath}, f)

    def loadConfigPath(self) -> str | None:
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            return json.load(f).get("config_path")
