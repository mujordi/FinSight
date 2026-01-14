
def macro_core(d):
    score=0; params=[]
    def add(n,v,s,i,e):
        nonlocal score; score+=i
        params.append({"name":n,"value":round(v,2),"signal":s,"impact":i,"explanation":e})

    add("Real Yield 10Y (%)",d["real_yield"],"positive" if d["real_yield"]<0 else "neutral" if d["real_yield"]<1 else "negative",
        2 if d["real_yield"]<0 else 1 if d["real_yield"]<1 else 0,"Cost of capital")
    add("Inflation YoY (%)",d["inflation"],"positive" if d["inflation"]<3 else "neutral" if d["inflation"]<4 else "negative",
        2 if d["inflation"]<3 else 1 if d["inflation"]<4 else 0,"Price stability")
    add("Yield Curve (10Y-2Y)",d["curve"],"positive" if d["curve"]>0 else "negative",
        1 if d["curve"]>0 else 0,"Growth expectations")
    add("Dollar Index",d["dxy"],"positive" if d["dxy"]<100 else "neutral" if d["dxy"]<105 else "negative",
        2 if d["dxy"]<100 else 1 if d["dxy"]<105 else 0,"Global liquidity")
    add("VIX",d["vix"],"positive" if d["vix"]<15 else "neutral" if d["vix"]<25 else "negative",
        2 if d["vix"]<15 else 1 if d["vix"]<25 else 0,"Risk appetite")

    state="RISK-ON" if score>=8 else "TRANSITION" if score>=4 else "RISK-OFF"
    return {"state":state,"score":score,"parameters":params}
