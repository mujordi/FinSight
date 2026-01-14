
def gold_model(macro):
    score = 0
    if macro["details"]["real_yield"] == "supportive": score += 2
    if macro["details"]["dxy"] == "weak": score += 2
    if macro["details"]["risk"] == "stress": score += 1

    state = "BULLISH" if score >= 4 else "NEUTRAL" if score >= 2 else "UNFAVORABLE"

    return {
        "state": state,
        "score": score,
        "explanation": "Gold benefits from low real yields, a weak dollar, and risk-off regimes."
    }
