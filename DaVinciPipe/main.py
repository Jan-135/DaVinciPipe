import json
import sys
from pathlib import Path
from typing import Any, Dict

from PySide6.QtGui import QIcon

from ui.mainUi import MainUi
from ui.style import appStyle

vendor = r"N:\vendor"
if vendor not in sys.path:
    sys.path.insert(0, vendor)

from DaVinciPipe.DavinciHandle import DavinciHandle
from DaVinciPipe.PipelineInterfaces import AbstractPipelineInterface, KitsuPipeline, ShotgridPipeline

from PySide6.QtWidgets import QApplication

mainWindow = None

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
    global mainWindow

    if config is None:
        config = _loadDefaultConfig()

    _addVendorToSyspath(config)
    print(sys.path)
    try:
        print(editingObject)
    except:
        raise Exception("Robin hat rein geschissen.")

    app = QApplication.instance()
    appWasCreatedHere = False
    if app is None:
        app = QApplication(sys.argv)
        appWasCreatedHere = True
    app.setStyleSheet(appStyle)
    iconPath = Path(__file__).parent.parent / "ui" / "icons" / "app.svg"
    print(iconPath)
    app.setWindowIcon(QIcon(str(iconPath)))

    try:
        manager: str = None
        pipe: AbstractPipelineInterface = None
        if config:
            manager = config.get("manager")
        if manager == "shotgrid":
            pipe = ShotgridPipeline() or None
        elif manager == "kitsu":
            config = config.get("kitsu")
            pipe = KitsuPipeline(app) or None
        else:
            print(f"[ERROR] Config error: unknown manager: {config.get('manager')}")
        if pipe is None:
            print("Pipe is None")
            return
        handle: DavinciHandle = DavinciHandle(pipe, editingObject, config)

        mainWindow = MainUi(handle=handle)
        mainWindow.show()

        if appWasCreatedHere:
            app.exec()
    except Exception as ex:
        print(ex)
        raise ex
