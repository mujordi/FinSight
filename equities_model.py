
def equities_model(macro):
    factors=[]
    for f in ["Quality","Growth","High Beta"]:
        if macro["state"]=="RISK-ON":
            view="Attractive" if f!="High Beta" else "Selective"
        elif macro["state"]=="RISK-OFF":
            view="Attractive" if f=="Quality" else "Avoid"
        else:
            view="Selective"
        factors.append({"factor":f,"view":view})
    return factors
