"""
Snooze Tracker
Tracks consecutive snoozes to enforce water drinking after 2 snoozes
"""

import json
from pathlib import Path
from datetime import datetime

class SnoozeTracker:
    def __init__(self, data_file="data.json"):
        self.data_file = Path(data_file)
    
    def reset_snoozed_status(self):
        """Reset snooze count after user drinks water"""
        data = self._load_data()
        data["snooze_count"] = 0
        self._save_data(data)
    
    def increment_snooze(self):
        """Increment snooze count"""
        data = self._load_data()
        data["snooze_count"] = data.get("snooze_count", 0) + 1
        self._save_data(data)
        return data["snooze_count"]
    
    def get_snooze_count(self):
        """Get current snooze count"""
        data = self._load_data()
        return data.get("snooze_count", 0)
    
    def is_snooze_locked(self):
        """Check if snooze should be locked (3rd or more consecutive snooze)"""
        return self.get_snooze_count() >= 2
    
    def _load_data(self):
        """Load data.json"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"snooze_count": 0}
    
    def _save_data(self, data):
        """Save to data.json"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
