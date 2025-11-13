# C:\Users\xy123\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\

import traceback
import sys
sys.path.append("N:/vendor")
REPO = r"K:\pipeline\DaVinciPipe"
if REPO not in sys.path:
    sys.path.insert(0, REPO)
try:
    from DaVinciPipe.main import main
    main(resolve)
except Exception as e:
    print("Fehler in DaVinciPipe:", e)
    traceback.print_exc()
