
import json, datetime

def update(state):
    try:
        h = json.load(open("history.json"))
    except:
        h = []
    h.append({
        "date": state["date"],
        "state": state["macro"]["state"],
        "score": state["macro"]["score"],
    })
    json.dump(h, open("history.json", "w"), indent=2)
