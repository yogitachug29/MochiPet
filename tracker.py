import json
import os
from datetime import date
from pathlib import Path

from settings import WATER_GOAL

APPDATA_DIR = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "MochiPet"
APPDATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = APPDATA_DIR / "data.json"
LEGACY_DATA_FILE = Path(__file__).resolve().parent / "data.json"


def _get_data_file():
    """Resolve the data file path and migrate legacy data if needed."""
    if DATA_FILE.exists():
        return DATA_FILE

    if LEGACY_DATA_FILE.exists() and not DATA_FILE.exists():
        try:
            with LEGACY_DATA_FILE.open("r") as file:
                data = json.load(file)
            save_data(data)
            return DATA_FILE
        except (OSError, json.JSONDecodeError):
            pass

    return DATA_FILE


def load_data():

    file_path = _get_data_file()

    if not file_path.exists():
        return {
            "date": str(date.today()),
            "water": 0
        }

    with file_path.open("r") as file:
        return json.load(file)


def save_data(data):

    file_path = _get_data_file()

    with file_path.open("w") as file:
        json.dump(data, file, indent=4)


def reset_if_new_day():

    data = load_data()

    today = str(date.today())

    if data["date"] != today:

        data["date"] = today
        data["water"] = 0

        save_data(data)

    return data


def add_water(amount):

    data = reset_if_new_day()

    data["water"] += amount

    save_data(data)


def get_water():

    data = reset_if_new_day()

    return data["water"]


def remaining_water():

    water = get_water()

    remaining = WATER_GOAL - water

    if remaining < 0:
        remaining = 0

    return remaining


def progress():

    water = get_water()

    return f"{water/1000:.2f} L / {WATER_GOAL/1000:.1f} L"