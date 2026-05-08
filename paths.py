import os
import sys
from pathlib import Path

# I will be using this for setting up storage system like actual applications .-.

APP_NAME = "TerminalPlay"

def get_app_dir() -> Path:
    home = Path.home()
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local")) / APP_NAME
    elif sys.platform == "darwin":
        return home / "library" / "Application Support" / APP_NAME
    else:
        return Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share")) / APP_NAME
    
DATA_DIR = get_app_dir()
ASSETS_DIR = DATA_DIR / "assets"
LIBRARY_FILE = DATA_DIR / "library.json" # our songs folder