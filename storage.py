
import json
FILE = "macro_state.json"

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
