from abc import ABC, abstractmethod
from typing import Any

from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface


class AbstractEditingSoftwareHandle(ABC):
    def __init__(self, pipe: AbstractPipelineInterface, config: dict):
        self._pipe = pipe
        self._config = config

    @property
    def pipe(self) -> AbstractPipelineInterface:
        return self._pipe

    @property
    def config(self) -> dict:
        return self._config


    @abstractmethod
    def getTimelineInfo(self) -> list[dict[str, Any]]:
        raise NotImplementedError()

    @abstractmethod
    def importShotCollection(self, shotCollection: list[dict[str, Any]]):
        raise NotImplementedError()

class BlenderHandle(AbstractEditingSoftwareHandle):

    def __init__(self, pipe: AbstractPipelineInterface, config: dict, bpyObj):
        self._bpy = bpyObj
        self._scene = None
        self._sequenceEditor = None


    @property
    def bpy(self):
        return self._bpy
    @property
    def scene(self):
        if self._scene is None:
            self._scene = self._bpy.context.scene
        return self._scene
    @property
    def sequenceEditor(self):
        if self._sequenceEditor is None:
            self._sequenceEditor = self.scene.sequence_editor
        return self._sequenceEditor

    def getTimelineInfo(self) -> list[dict[str, Any]]:
        pass

    def importShotCollection(self, shotCollection: list[dict[str, Any]]):
        import pdb; pdb.set_trace()
        for shot in shotCollection:
            print(shot.get("filePath"))
            if shot.get("filePath"):
                print("INSIDE")
                movieStrip = self.sequenceEditor.sequences.new_movie(
                   name = shot["name"],
                   filepath = str(shot["filePath"]),
                   channel = 1,
                   frame_start = shot["start"],
                )
                print(movieStrip)