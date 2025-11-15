import json
import pathlib
import re
from abc import ABC, abstractmethod
from typing import Any, Optional

import gazu
from PySide6.QtWidgets import QDialog

from DaVinciPipe.storage.ConfigStore import ConfigStore
from DaVinciPipe.storage.CredentialStore import CredentialStore
from ui.loginWindow import LoginDialog


class AbstractPipelineInterface(ABC):

    def getShotInformations(self):
        shotList = self._collectShotsFromPipeline()
        if self.__validate(shotList):
            return shotList
        else:
            raise Exception('Shot information not valid')

    def __validate(self, shotList):
        for shot in shotList:
            if shot.get("name") and shot.get("start") and shot.get("duration") and shot.get("end") and shot.get("path"):
                continue
            else:
                return False
        return True

    @abstractmethod
    def _collectShotsFromPipeline(self) -> list[dict[str, Any]]:
        """
        Needs to be implemented to collect the shots from the database
        (e.g. Shotgrid / Kitsu)
        """
        pass

    @abstractmethod
    def updateAllShots(self, shotList: list[dict[str, Any]]) -> bool:
        """
        Needs to be implemented to update the shots from the database
        :param shotList:
        :return:
        """
        pass

    @abstractmethod
    def updateShot(self, shot) -> bool:
        pass


class ShotgridPipeline(AbstractPipelineInterface):
    pass


class KitsuPipeline(AbstractPipelineInterface):

    def __init__(self, qtApp):
        self._qtApp = qtApp
        self.configStore = ConfigStore()
        self.credentials = CredentialStore()

        # Load stored config path (optional)
        storedConfigPath = self.configStore.loadConfigPath()
        loaded_config = None

        if storedConfigPath:
            try:
                with open(storedConfigPath, "r") as f:
                    loaded_config = json.load(f)
            except Exception as e:
                print(f"[ERROR] Stored config corrupted: {e}")
                storedConfigPath = None
                loaded_config = None

        # Try saved tokens + saved config
        saved_tokens = self.credentials.loadSession()
        if saved_tokens and loaded_config:
            api_url = loaded_config.get("kitsu").get("apiUrl")
            if api_url:
                gazu.client.set_host(api_url)
                gazu.client.default_client.tokens = saved_tokens

                try:
                    gazu.client.get_current_user()
                    print("[INFO] Auto-login successful using stored config + tokens")
                    self.config = loaded_config.get("kitsu")
                    self.passedLogin = True
                    return
                except:
                    print("[WARNING] Saved session invalid")
            else:
                print("[WARNING] Stored config missing apiUrl")

        # 3. Show login dialog (pass stored config)
        dlg = LoginDialog(config=loaded_config)

        if dlg.exec() != QDialog.Accepted:
            print("[ERROR] Login canceled")
            self.passedLogin = False
            return

        # 4. Retrieve config path + load config
        config_path = dlg.getConfigPath()
        if not config_path:
            print("[ERROR] No config selected")
            self.passedLogin = False
            return

        with open(config_path, "r") as f:
            new_config = json.load(f).get("kitsu", "")

        # 5. Save chosen config path
        self.configStore.saveConfigPath(config_path)

        # 6. Save tokens after successful login
        self.credentials.saveSession(gazu.client.default_client.tokens)

        # 7. Store final config
        self.config = new_config
        print("[INFO] Login + config selection successful")
        self.passedLogin = True

    def _collectShotsFromPipeline(self) -> list[dict[str, Any]]:
        project = self._getProject()
        shotListOut = []

        filter = {
            "project_id": project["id"]
        }
        kitsuShotList = gazu.client.get(path="data/shots", params=filter)

        for kitsuShot in kitsuShotList:
            id = kitsuShot["id"]
            shot = gazu.shot.get_shot(id)
            if shot is None or shot.get("data") is None:
                continue
            else:
                name = shot["sequence_name"] + "_" + shot["name"]
                filePath = self._getFilePath(folderPath=shot.get("data").get("absolutepath"), shotName=name)
                if filePath is None:
                    print(f"[WARNING] Could not find file for shot: {name}")

                outShot = {
                    "name": name,
                    "start": shot["frame_in"],
                    "end": shot["frame_out"],
                    "duration": shot["nb_frames"],
                    "filePath": filePath
                }

                shotListOut.append(outShot)

        return shotListOut

    def updateAllShots(self, shotList: list[dict[str, Any]]) -> bool:
        return True

    def updateShot(self, shot) -> bool:
        return True

    ### HELPER ###

    def _getFilePath(self, folderPath: str, shotName: str) -> Optional[str]:
        if folderPath is None or "":
            return None
        p = pathlib.Path(folderPath)
        if not p.exists() or not p.is_dir():
            return None

        pattern = re.compile(
            r"^(?P<camera>[A-Za-z0-9.]+)_(?P<shot>[A-Za-z0-9]+)_(?P<task>[A-Za-z][A-Za-z0-9_-]*)(?=_v)_v(?P<ver>\d{3,})\.(?P<ext>[A-Za-z0-9]+)$",
            re.IGNORECASE
        )

        bestVersion = -1
        newestTask = 0
        bestPath = None

        for file in p.iterdir():

            if not file.is_file():
                continue

            m = pattern.match(file.name)
            if not m:
                continue

            info = m.groupdict()

            versionNumber = int(info["ver"])

            if versionNumber > bestVersion:
                bestVersion = versionNumber
                bestPath = file

        return bestPath

    def _getProject(self):
        projectName = self.config.get("project_name")
        print(f"config: {self.config}")
        print(f"projectName = {projectName}")
        allProjects = gazu.client.get("/data/projects/all")
        print(f"All projects : {[project['name'] for project in allProjects]}")
        kitsuProject = [project for project in allProjects if project["name"] == projectName][0]
        return kitsuProject
