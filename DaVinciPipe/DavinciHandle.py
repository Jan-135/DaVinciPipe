from typing import Any

from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface


class DavinciHandle:
    def __init__(self, pipe: AbstractPipelineInterface) -> None:
        self.pipe = pipe

    def getTimelineInfo(self, timeline) -> list[dict[str, Any]]:
        print(timeline)
        print(dir(timeline))
        clipsCollection = []
        for trackType in ("video", "audio"):
            for t in range(1, (timeline.GetTrackCount(trackType) or 0) + 1):
                for item in (timeline.GetItemListInTrack(trackType, t) or []):
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

        print(f"Timeline: {timeline.GetName()} | Clips: {len(clipsCollection)}")
        for i, c in enumerate(clipsCollection, 1):
            print(f'{i:02d} | {c["trackType"]}{c["trackIndex"]} | {c["name"]} | {c["start"]}-{c["end"]}')

        return clipsCollection

    def updateClip(self, shot) -> bool:
        return self.pipe.updateShot(shot)

