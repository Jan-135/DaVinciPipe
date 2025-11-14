import json
import sys
from pathlib import Path
from typing import Any, Dict

vendor = r"N:\vendor"
if vendor not in sys.path:
    sys.path.insert(0, vendor)

from DaVinciPipe.DavinciHandle import DavinciHandle
from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface, KitsuPipeline, ShotgridPipeline

from PySide6.QtWidgets import QApplication


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


def main(editingObject, config: dict[str, Any] = None):
    if config is None:
        config = _loadDefaultConfig()

    _addVendorToSyspath(config)
    print(sys.path)
    try:
        print(editingObject)
    except:
        raise Exception("Robin hat rein geschissen.")

    qtApp = QApplication.instance() or QApplication([])
    QApplication.setQuitOnLastWindowClosed(False)

    try:
        manager: str = None
        pipe: AbstractPipelineInterface = None
        if config:
            manager = config.get("manager")
        if manager == "shotgrid":
            pipe = ShotgridPipeline() or None
        elif manager == "kitsu":
            print(1)
            pipe = KitsuPipeline(config.get("kitsu"), qtApp) or None
            print(2)
        if pipe is None:
            print("Pipe is None")
            return
        handle: DavinciHandle = DavinciHandle(pipe, editingObject, config)

        kitsuShots = pipe._collectShotsFromPipeline()
        handle.importShotCollection(kitsuShots)
    except Exception as ex:
        print(ex)
        raise ex
