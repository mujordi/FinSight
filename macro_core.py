
def macro_core(d):
    score=0; params=[]
    def add(n,v,s,i,e):
        nonlocal score; score+=i
        params.append({"name":n,"value":round(v,2),"signal":s,"impact":i,"explanation":e})

    add("Real Yield 10Y",d["real_yield"],"negative" if d["real_yield"]>1 else "neutral",0,"Cost of capital")
    add("Inflation YoY",d["inflation"],"positive" if d["inflation"]<3 else "neutral",1,"Price stability")
    add("Yield Curve",d["curve"],"positive" if d["curve"]>0 else "negative",1,"Growth signal")
    add("Dollar Index",d["dxy"],"negative" if d["dxy"]>105 else "neutral",0,"Liquidity")
    add("VIX",d["vix"],"positive" if d["vix"]<20 else "neutral",1,"Risk appetite")

    state="RISK-ON" if score>=3 else "TRANSITION"
    return {"state":state,"score":score,"parameters":params}
