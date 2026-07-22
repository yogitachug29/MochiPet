"""
Auto-Updater for MochiPet
Checks for new versions and updates the app automatically
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from urllib import request, error as url_error
from threading import Thread
import time

# Configuration
CURRENT_VERSION = "1.0"
GITHUB_REPO = "yogitachug29/MochiPet"  # Replace with your GitHub username/repo
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def get_installed_exe_path():
    """Get the path to the installed MochiPet executable"""
    if getattr(sys, 'frozen', False):
        # App is frozen by PyInstaller
        return sys.executable
    return None

def get_version_from_server():
    """Fetch the latest version info from server"""
    try:
        print("Checking URL:", UPDATE_CHECK_URL)

        response = request.urlopen(UPDATE_CHECK_URL, timeout=5)
        print("Response received")

        data = json.loads(response.read().decode())
        print("Latest version:", data["tag_name"])

        # For GitHub releases, extract version from tag
        if "tag_name" in data:
            return data["tag_name"].lstrip("v"), data.get("assets", [])

        # For custom server
        return data.get("version"), data.get("download_url")

    except Exception as e:
        print(f"Update check failed: {e}")
        return None, None

def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        print(f"Downloading from {url}...")
        request.urlretrieve(url, destination)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def update_exe(new_exe_path):
    """Replace the current executable with the new one"""
    try:
        current_exe = get_installed_exe_path()
        if not current_exe:
            return False
        
        # Create backup of current exe
        backup_path = f"{current_exe}.backup"
        shutil.copy2(current_exe, backup_path)
        
        # Replace with new version
        shutil.copy2(new_exe_path, current_exe)
        
        # Clean up temp file
        if os.path.exists(new_exe_path):
            os.remove(new_exe_path)
        
        print("Update successful!")
        return True
    except Exception as e:
        print(f"Update failed: {e}")
        return False

def restart_app():
    """Restart the current application"""
    current_exe = get_installed_exe_path()
    if current_exe:
        subprocess.Popen([current_exe])
        sys.exit()

def check_and_update():
    """Check for updates and install if available"""
    try:
        latest_version, download_info = get_version_from_server()

        if not latest_version:
            return

        print(f"Current version: {CURRENT_VERSION}")
        print(f"Latest version: {latest_version}")

        # Compare versions
        if is_newer_version(latest_version, CURRENT_VERSION):
            print("Update available!")

            # Prepare download URL
            if isinstance(download_info, list) and len(download_info) > 0:
                download_url = next(
                    (asset["browser_download_url"] for asset in download_info
                     if asset["name"].endswith(".exe")),
                    None
                )
            else:
                download_url = download_info

            print("Download URL:", download_url)

            if download_url:
                temp_exe = os.path.join(
                    os.path.expanduser("~"),
                    "AppData", "Local", "Temp",
                    "MochiPet_update.exe"
                )

                if download_file(download_url, temp_exe):
                    if update_exe(temp_exe):
                        print("Restarting application...")
                        restart_app()
        else:
            print("Already on the latest version.")

    except Exception as e:
        print(f"Update check error: {e}")
        
def is_newer_version(new_version, current_version):
    """Compare version strings (e.g., '1.1' > '1.0')"""
    try:
        new_parts = [int(x) for x in new_version.lstrip('v').split('.')]
        current_parts = [int(x) for x in current_version.split('.')]
        
        # Pad with zeros if lengths differ
        max_len = max(len(new_parts), len(current_parts))
        new_parts.extend([0] * (max_len - len(new_parts)))
        current_parts.extend([0] * (max_len - len(current_parts)))
        
        return new_parts > current_parts
    except:
        return False

def start_update_check():
    """Start update check in background thread"""
    thread = Thread(target=check_and_update, daemon=True)
    thread.start()
