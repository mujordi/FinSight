
def assets(state):
    return [
        {"name":"Cash","view":"Neutral" if state!="RISK-OFF" else "Attractive","color":"yellow"},
        {"name":"Bonds","view":"Attractive" if state!="RISK-ON" else "Neutral","color":"green"},
        {"name":"Gold","view":"Attractive" if state!="RISK-ON" else "Neutral","color":"green"},
        {"name":"Equities","view":"Selective" if state!="RISK-ON" else "Attractive","color":"yellow"},
        {"name":"High Beta","view":"Avoid" if state=="RISK-OFF" else "Selective","color":"red"}
    ]
