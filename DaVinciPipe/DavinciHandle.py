import copy
from pathlib import Path
from typing import Any, Optional

from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface


class DavinciHandle:
    def __init__(self, pipe: AbstractPipelineInterface, resolve, config: dict) -> None:

        self._pipe = pipe
        self._config = config

        # Resolve Objects:
        self._resolve = resolve
        self._projectManager = None
        self._project = None
        self._mediaStorage = None
        self._fusion = None
        self._mediaPool = None
        self._timeline = None

        self._fps = None
        self._shotCollection = None

    @property
    def pipe(self):
        return self._pipe

    @property
    def config(self):
        return copy.deepcopy(self._config)

    @property
    def resolve(self):
        if self._resolve is None:
            raise RuntimeError("Resolve instance not initialized.")
        return self._resolve

    @property
    def projectManager(self):
        if self._projectManager is None:
            self._projectManager = self.resolve.GetProjectManager()
        return self._projectManager

    @property
    def project(self):
        if self._project is None:
            self._project = self.projectManager.GetCurrentProject()
        return self._project

    @property
    def mediaStorage(self):
        if self._mediaStorage is None:
            self._mediaStorage = self.resolve.GetMediaStorage()
        return self._mediaStorage

    @property
    def fusion(self):
        if self._fusion is None:
            self._fusion = self.resolve.GetFusion()
        return self._fusion

    @property
    def mediaPool(self):
        if self._mediaPool is None:
            self._mediaPool = self.project.GetMediaPool()
        return self._mediaPool

    @property
    def timeline(self):
        if self._timeline is None:
            self._timeline = self.project.GetTimelineByIndex(1)
        return self._timeline

    @property
    def fps(self):
        if self._fps is None:
            self._fps = self.project.GetSetting("timelineFrameRate")
        return self._fps

    @property
    def shotCollection(self) -> list[dict[str, Any]] :
        if self._shotCollection is None:
            self._shotCollection = self.pipe.getShotInformations()
        return self._shotCollection

    def getTimelineInfo(self) -> list[dict[str, Any]]:
        clipsCollection = []
        for trackType in ("video", "audio"):
            for t in range(1, (self.timeline.GetTrackCount(trackType) or 0) + 1):
                for item in (self.timeline.GetItemListInTrack(trackType, t) or []):
                    mediaPool = item.GetMediaPoolItem()
                    clipsCollection.append({
                        "name": item.GetName(),
                        "trackType": trackType,
                        "trackIndex": t,
                        "start": item.GetStart(),
                        "end": item.GetEnd() - 1,
                        "duration": item.GetDuration(),
                        "mediaName": mediaPool.GetName() if mediaPool else None,
                        "filePath": (mediaPool.GetClipProperty("File Path") if mediaPool else None),
                    })

        return clipsCollection

    def importShotCollection(self):

        clipInfos = []
        for shot in self.shotCollection:
            if shot.get("filePath"):
                item = self._importShotViaFilePath(shot)
                if item is not None:
                    recordFrame = self._startFrame() + shot["start"]
                    print("[DEBUG]")
                    print(f"RecordFrame for shot {shot['name']}: {recordFrame}")
                    clipInfo = {
                        "mediaPoolItem": item,
                        "trackIndex": 1,
                        "recordFrame": recordFrame,
                    }
                    clipInfos.append(clipInfo)

        self.mediaPool.AppendToTimeline(clipInfos)

    def _startFrame(self):
        """Davinci starts frame count at 1 hour"""
        return self.fps * 3600

    def _importShotViaFilePath(self, shot: dict[str, Any]) -> Optional[any]:
        filePath: Path = shot.get("filePath")
        if filePath is None:
            return None
        addedItems = self.mediaStorage.AddItemListToMediaPool([str(filePath)])
        return addedItems[0]

    def updateClip(self, shot) -> bool:
        return self._pipe.updateShot(shot)

    def getPlaceholderItem(self, shot, comp):

        background = comp.AddTool("Background")
        text = comp.AddTool("TextPlus")
        merge = comp.AddTool("Merge")

        merge.ConnectInput("Background", background)
        merge.ConnectInput("Foreground", text)

        return merge

    def _frameToTimeCode(self, frame, fps=None, oneHourOffsetAlreadyAdded=True) -> str:
        if fps is None:
            fps = self._fps

        f = int(frame)
        h = f // int(fps * 3600)
        f %= int(fps * 3600)
        m = f // int(fps * 60)
        f %= int(fps * 60)
        s = f // int(fps)
        f %= int(fps)
        if not oneHourOffsetAlreadyAdded:
            h += 1  # Resolve starts at 1 hour
        return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"
