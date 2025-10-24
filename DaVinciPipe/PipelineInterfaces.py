from abc import ABC, abstractmethod
from typing import Any

import gazu


class AbstractPipelineInterface(ABC):

    def getShotInformations(self):
        shotList = self._collectShots()
        if self.__validate(shotList):
            return shotList
        else:
            raise Exception('Shot information not valid')

    def __validate(self, shotList):
        for shot in shotList:
            if shot.get("name") and shot.get("start") and shot.get("duration") and shot.get("end"):
                return True
            else:
                return False

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

    def __init__(self, config: dict):
        """
                Connects to Kitsu server using the username and password given in the config file.

                :param config:
                :return:
                """
        self.config = config
        try:
            apiUrl = config.get("apiUrl")
            email = config.get('email')
            password = config.get('password')
            if not apiUrl or not email or not password:
                raise Exception("apiUrl, email and password are required in config.yaml")

            gazu.client.set_host(apiUrl)
            gazu.log_in(config["email"], config["password"])
        except gazu.exception.AuthFailedException as e:
            print(f"Authentication Error while connecting to {apiUrl} as {email}.")
            raise e

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

                outShot = {
                    "name": shot["sequence_name"] + "_" + shot["name"],
                    "start": shot["frame_in"],
                    "end": shot["frame_out"],
                    "duration": shot["nb_frames"],
                    "filePath": shot.get("data").get("absolutepath")
                }

                shotListOut.append(outShot)

        return shotListOut

    def updateAllShots(self, shotList: list[dict[str, Any]]) -> bool:
        return True

    def updateShot(self, shot) -> bool:
        return True

    ### HELPER ###

    def _getProject(self):
        projectName = self.config.get("project_name")
        allProjects = gazu.client.get("/data/projects/all")
        kitsuProject = [project for project in allProjects if project["name"] == projectName][0]
        return kitsuProject
