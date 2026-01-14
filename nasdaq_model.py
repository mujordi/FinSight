
def nasdaq_model(macro):
    score = 0
    if macro["details"]["real_yield"]!="restrictive": score+=2
    if macro["details"]["risk"]=="calm": score+=2
    if macro["details"]["dxy"]!="strong": score+=1

    if score>=4:
        state="BULLISH"
    elif score>=2:
        state="NEUTRAL"
    else:
        state="UNFAVORABLE"

    return {
        "state": state,
        "score": score,
        "explanation": "Growth assets perform best with supportive rates, calm volatility and liquidity."
    }
