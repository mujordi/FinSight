
import json
FILE = "macro_state.json"

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def load():
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {}
