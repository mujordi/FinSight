
def macro_model(inputs):
    score = 0
    details = {}

    if inputs["real_yield"] < 0:
        score += 2; details["real_yield"] = "supportive"
    elif inputs["real_yield"] < 1:
        score += 1; details["real_yield"] = "neutral"
    else:
        details["real_yield"] = "restrictive"

    if inputs["dxy"] < 100:
        score += 2; details["dxy"] = "weak"
    elif inputs["dxy"] < 105:
        score += 1; details["dxy"] = "neutral"
    else:
        details["dxy"] = "strong"

    if inputs["vix"] > 25:
        score += 2; details["risk"] = "stress"
    elif inputs["vix"] > 15:
        score += 1; details["risk"] = "normal"
    else:
        details["risk"] = "calm"

    state = "RISK FAVORABLE" if score >= 5 else "TRANSITION" if score >= 3 else "RISK RESTRICTIVE"

    return {
        "state": state,
        "score": score,
        "explanation": "Macro regime based on real yields, dollar strength and risk conditions.",
        "details": details
    }
