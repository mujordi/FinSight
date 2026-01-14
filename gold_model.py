
def gold_model(macro):
    score = 0
    if macro["details"]["real_yield"]=="supportive": score+=2
    if macro["details"]["dxy"]=="weak": score+=2
    if macro["details"]["risk"]=="stress": score+=1

    if score>=4:
        state="BULLISH"
    elif score>=2:
        state="NEUTRAL"
    else:
        state="UNFAVORABLE"

    return {
        "state": state,
        "score": score,
        "explanation": "Gold benefits from low real yields, weak dollar and risk-off regimes."
    }
