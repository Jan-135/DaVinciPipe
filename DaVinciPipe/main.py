import json
from pathlib import Path
from typing import Any, Dict

from DaVinciPipe.DavinciHandle import DavinciHandle
from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface, KitsuPipeline, ShotgridPipeline

import sys


def _addVendorToSyspath(config: dict[str, Any]) -> None:
    vendorsPathRaw = config.get("vendorsPath")
    if not vendorsPathRaw:
        raise ValueError("config['vendorsPath'] missing.")
    vendorsPath = Path(vendorsPathRaw).expanduser().resolve()
    if not vendorsPath.exists():
        raise FileNotFoundError(f"Could not find Vendor-Folder: {vendorsPath}")
    vendorStr = str(vendorsPath)
    if vendorStr not in sys.path:
        sys.path.insert(0, vendorStr)


def _loadDefaultConfig() -> Dict[str, Any]:
    base = Path(__file__).resolve().parent
    configPath = base / ".." / "config" / "default.json"
    if not configPath.exists():
        raise FileNotFoundError(
            f"Could not find default config: {configPath}\n"
            f"(CWD): {Path.cwd()}"
        )
    with configPath.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(resolve, config: dict[str, Any] = None):
    if config is None:
        config = _loadDefaultConfig()

    _addVendorToSyspath(config)
    print(sys.path)
    try:
        print(resolve)
    except:
        raise Exception("Robin hat rein geschissen.")

    manager: str = None
    pipe: AbstractPipelineInterface = None

    if config:
        manager = config.get("manager")

    if manager == "shotgrid":
        pipe = ShotgridPipeline()
    elif manager == "kitsu":
        pipe = KitsuPipeline(config.get("kitsu"))

    handle: DavinciHandle = DavinciHandle(pipe)

    davinciProject = resolve.GetProjectManager().GetCurrentProject()
    timeline = davinciProject.GetTimelineByIndex(1)
    clipsCollection = handle.getTimelineInfo(timeline)
    kitsuShots = pipe._collectShotsFromPipeline()
    print(dir(kitsuShots))
