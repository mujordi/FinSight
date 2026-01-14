
def gold_model(macro):
    score=0; details=[]
    def add(n,s,i,e):
        nonlocal score; score+=i
        details.append({"name":n,"signal":s,"impact":i,"explanation":e})

    ry=next(p for p in macro["parameters"] if "Real Yield" in p["name"])
    usd=next(p for p in macro["parameters"] if "Dollar" in p["name"])

    add("Real Yields",ry["signal"],2 if ry["signal"]=="negative" else 0,"Gold inversely correlated to real yields")
    add("USD Strength",usd["signal"],2 if usd["signal"]=="negative" else 0,"Strong USD pressures gold")

    view="Attractive" if score>=2 else "Neutral"
    return {"score":score,"view":view,"drivers":details}
