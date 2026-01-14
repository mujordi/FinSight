
def assets(state):
    return [
        {"name": "Cash", "view": "Attractive" if state == "RISK-OFF" else "Neutral", "color": "green" if state == "RISK-OFF" else "yellow"},
        {"name": "Bonds", "view": "Attractive" if state != "RISK-ON" else "Neutral", "color": "green"},
        {"name": "Gold", "view": "Attractive" if state != "RISK-ON" else "Neutral", "color": "green"},
        {"name": "Equities", "view": "Attractive" if state == "RISK-ON" else "Selective", "color": "yellow"},
        {"name": "High Beta", "view": "Avoid" if state == "RISK-OFF" else "Selective", "color": "red"},
    ]
