import os
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path

# THIS WILL BE THE INSTALLER FILE WHICH WILL INSTALL the application in the user's pc and do all the configuration so user doesn't need to.


if sys.platform == "win32":
    import win32com.client
else:
    win32com = None


def get_app_path(): # This will return our data folder which will be C:/Users/{your user}/AppData/Local/TerminalPlay
    home = Path.home()
    if sys.platform == "win32":
        return Path(os.environ["LOCALAPPDATA"]) / "TerminalPlay"
    elif sys.platform == "darwin":
        return home / "Library" / "Application Support" / "TerminalPlay"
    else:
        return Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share")) / "TerminalPlay"
    

def create_shortcut(target, shortcut_path, install_dir): # This will create the shortcut in desktop
    home = Path.home()
    desktop = home / "Desktop"

    if not desktop.exists():
        desktop = None

    if sys.platform == "win32":
        # WINDOW
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = str(target.parent)
        shortcut.IconLocation = str(install_dir / "assets" / "icon.ico")
        shortcut.save()
        print(f"Window Shortcut created at '{shortcut_path}'")
    elif sys.platform == "linux":
        # LINUX
        shortcut_path = desktop / "TerminalPlayer.desktop"
        icon_path = install_dir / "assets" / "icon.png"
        if not icon_path.exists():
            icon_path = install_dir / "assets" / "icon.ico"

        desktop_entry = f"""[Desktop Entry]
Type=Application
Version=1.0
Name=TerminalPlayer
Comment=The Revolution in Terminal Audio
Exec=gnome-terminal -- {target}
Icon={icon_path}
Terminal=true
Categories=AudioVideo;Audio;Player;
"""
        with open(shortcut_path, "w", encoding="utf-8") as f:
            f.write(desktop_entry)
        
        shortcut_path.chmod(0o755)
        print(f"Linux Application Launcher created at {shortcut_path}")
    elif sys.platform == "darwin":
        # MAC OS
        shortcut_path = desktop / "TerminalPlayer"
        if shortcut_path.exists() or shortcut_path.is_symlink():
            shortcut_path.unlink()
        shortcut_path.symlink_to(target)
        print(f"macOS Symlink created at {shortcut_path}")

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