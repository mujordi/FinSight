
def macro_model(inputs):
    score = 0
    details = {}

    ry = inputs["real_yield"]
    if ry < 0:
        score += 2; details["real_yield"]="supportive"
    elif ry < 1:
        score += 1; details["real_yield"]="neutral"
    else:
        details["real_yield"]="restrictive"

    dxy = inputs["dxy"]
    if dxy < 100:
        score += 2; details["dxy"]="weak"
    elif dxy < 105:
        score += 1; details["dxy"]="neutral"
    else:
        details["dxy"]="strong"

    vix = inputs["vix"]
    if vix > 25:
        score += 2; details["risk"]="stress"
    elif vix > 15:
        score += 1; details["risk"]="normal"
    else:
        details["risk"]="calm"

    if score >= 5:
        state="RISK FAVORABLE"
    elif score >=3:
        state="TRANSITION"
    else:
        state="RISK RESTRICTIVE"

    return {
        "state": state,
        "score": score,
        "explanation": "Macro regime based on real yields, dollar strength and risk conditions.",
        "details": details
    }
