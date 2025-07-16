import json
from pathlib import Path

ACCESS_FILE = Path(__file__).parent / "storage.json"

def load_access_status():
    if not ACCESS_FILE.exists():
        return False
    with open(ACCESS_FILE, "r") as f:
        data = json.load(f)
    return data.get("access_granted", False)

def save_access_status(status: bool):
    with open(ACCESS_FILE, "w") as f:
        json.dump({"access_granted": status}, f)
