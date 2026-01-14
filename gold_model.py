
def gold_model(macro):
    score = 0
    reasons = {}

    # Real yields (key driver)
    ry = macro["details"]["real_yield"]
    if ry in ["favorable"]:
        score += 2
        reasons["real_yield"] = "supportive"
    elif ry in ["neutral"]:
        score += 1
        reasons["real_yield"] = "neutral"
    else:
        reasons["real_yield"] = "headwind"

    # Dollar
    dxy = macro["details"]["dxy"]
    if dxy == "favorable":
        score += 2
        reasons["dxy"] = "weak dollar"
    elif dxy == "neutral":
        score += 1
        reasons["dxy"] = "neutral"
    else:
        reasons["dxy"] = "strong dollar"

    # Risk / stress
    vix = macro["details"]["vix"]
    if vix == "estrès":
        score += 2
        reasons["risk"] = "risk-off hedge"
    elif vix == "normal":
        score += 1
        reasons["risk"] = "neutral"
    else:
        reasons["risk"] = "risk-on"

    if score >= 5:
        state = "GOLD STRONG BULLISH"
    elif score >= 3:
        state = "GOLD NEUTRAL / HOLD"
    else:
        state = "GOLD UNFAVORABLE"

    return {
        "gold_state": state,
        "score": score,
        "reasons": reasons
    }
