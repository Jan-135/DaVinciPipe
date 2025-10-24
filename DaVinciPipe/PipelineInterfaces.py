import pathlib
import re
from abc import ABC, abstractmethod
from typing import Any, Optional

import gazu
import sys

sys.path.append("N:/vendor")

from PySide6.QtWidgets import QDialog

from ui.login_window import LoginDialog


class AbstractPipelineInterface(ABC):

    def getShotInformations(self):
        shotList = self._collectShotsFromPipeline()
        if self.__validate(shotList):
            return shotList
        else:
            raise Exception('Shot information not valid')

    def __validate(self, shotList):
        for shot in shotList:
            if shot.get("name") and shot.get("start") and shot.get("duration") and shot.get("end"):
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

    def __init__(self, config: dict, qtApp):
        self.config = config
        self._qtApp = qtApp
        dlg = LoginDialog(apiUrl=self.config.get("apiUrl"))
        if dlg.exec() == QDialog.Accepted:
            self.passedLogin = True
        else:
            self.passedLogin = False

    def _connect(self) -> bool:
            email = None
            try:
                apiUrl = self.config.get("apiUrl")
                login = LoginDialog()
                login.show()
                if login.exec() == QDialog.Accepted:
                    email, password = login.get_credentials()
                else:
                    return True

                if not apiUrl or not email or not password:
                    raise Exception("apiUrl, email and password are required in config.yaml")

                gazu.client.set_host(apiUrl)
                gazu.log_in(email, password)
            except gazu.exception.AuthFailedException as e:
                return False
            return True

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
                print(f"Shot {id} not found.")
                print(kitsuShot)
            else:
                name = shot["sequence_name"] + "_" + shot["name"]
                filePath = self._getFilePath(folderPath=shot.get("data").get("absolutepath"), shotName=name)
                if filePath is None:
                    print(f"Could not find file for shot: {name}")

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
        p = pathlib.Path(folderPath)
        if not p.exists() or not p.is_dir():
            return None

        pattern = re.compile(
            r'^active_(?P<shot>[A-Za-z0-9]+)_(?P<task>[A-Za-z][A-Za-z0-9-]*)_v(?P<ver>\d{3,})\.(?P<ext>[A-Za-z0-9]+)$',
            re.IGNORECASE
        )

        bestVersion = -1
        bestPath = None

        for file in p.iterdir():

            if not file.is_file():
                continue

            m = pattern.match(file.name)
            if not m:
                continue

            info = m.groupdict()
            key = f"{info['shot']}_{info['task']}"

            if key.casefold() != shotName.casefold():
                continue

            versionNumber = int(info["ver"])

            if versionNumber > bestVersion:
                bestVersion = versionNumber
                bestPath = file

        return bestPath

    def _getProject(self):
        projectName = self.config.get("project_name")
        allProjects = gazu.client.get("/data/projects/all")
        kitsuProject = [project for project in allProjects if project["name"] == projectName][0]
        return kitsuProject
