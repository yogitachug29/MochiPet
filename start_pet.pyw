import os
import subprocess
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "main.py")
VENV_PYTHONW = os.path.join(SCRIPT_DIR, ".venv", "Scripts", "pythonw.exe")


def launch_pet():
    if os.path.exists(VENV_PYTHONW):
        subprocess.Popen(
            [VENV_PYTHONW, MAIN_SCRIPT],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0,
        )
    else:
        subprocess.Popen(
            [sys.executable, MAIN_SCRIPT],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=0,
        )


if __name__ == "__main__":
    launch_pet()
