import os
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path
import win32com.client

# THIS WILL BE THE INSTALLER FILE WHICH WILL INSTALL the application in the user's pc and do all the configuration so user doesn't need to.

def get_app_path(): # This will return our data folder which will be C:/Users/{your user}/AppData/Local/TerminalPlay
    return Path(os.environ["LOCALAPPDATA"]) / "TerminalPlay"

def create_shortcut(target, shortcut_path, install_dir): # This will create the shortcut in desktop
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(shortcut_path))
    shortcut.TargetPath = str(target)
    shortcut.WorkingDirectory = str(target.parent)
    shortcut.IconLocation = str(install_dir / "assets" / "icon.ico")
    shortcut.save()

def run_install(): # Main installer function
    install_dir = get_app_path()
    install_dir.mkdir(parents=True, exist_ok=True)

    print(f"Installing Terminal Play at '{install_dir}'")
    EXE_URL = "https://github.com/ProHeartly/terminal-play/releases/download/v0.1.6-alpha/main.exe" # Main application
    ASSETS_URL = "https://github.com/ProHeartly/terminal-play/releases/download/v0.1.6-alpha/assets.zip" # Assets folder

    try:
        print("Downloading the engine...")
        urllib.request.urlretrieve(EXE_URL, install_dir / "main.exe")

        print("Downloading assets...")
        zip_path = install_dir / "assets.zip"
        urllib.request.urlretrieve(ASSETS_URL, zip_path)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)

        os.remove(zip_path) # Clean up the zip of asset

        print("Creating shortcut of application...")
        desktop = Path(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        create_shortcut(install_dir / "main.exe", desktop / "TerminalPlayer.lnk", install_dir)

        print("TERMINAL PLAYER IS INSTALLED!!!\n\n")
        print("You can find it in your desktop..\n\n\n")
        input("Press Enter to exit.....")

    except Exception as e:
        print(f"INSTALLATION FAILED: {e}\n\n\n")
        input("Press Enter to cry...")

if __name__ == "__main__":
    run_install()