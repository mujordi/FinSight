
def macro_model(inputs):
    score = 0
    parameters = []

    def add(param, raw, signal, impact, explanation):
        nonlocal score
        score += impact
        parameters.append({
            "parameter": param,
            "real_value": raw,
            "signal": signal,
            "impact": impact,
            "explanation": explanation
        })

    ry = inputs["real_yield"]
    if ry < 0:
        add("Real Yield (10Y)", ry, "positive", 2, "Negative real yields lower opportunity cost of risk assets.")
    elif ry < 1:
        add("Real Yield (10Y)", ry, "neutral", 1, "Moderate real yields are macro-neutral.")
    else:
        add("Real Yield (10Y)", ry, "negative", 0, "High real yields tighten financial conditions.")

    dxy = inputs["dxy"]
    if dxy < 100:
        add("US Dollar Index (DXY)", dxy, "positive", 2, "Weak dollar supports global liquidity.")
    elif dxy < 105:
        add("US Dollar Index (DXY)", dxy, "neutral", 1, "Stable dollar is neutral for risk.")
    else:
        add("US Dollar Index (DXY)", dxy, "negative", 0, "Strong dollar restricts liquidity.")

    vix = inputs["vix"]
    if vix < 15:
        add("Equity Volatility (VIX)", vix, "positive", 2, "Low volatility indicates risk-on regime.")
    elif vix < 25:
        add("Equity Volatility (VIX)", vix, "neutral", 1, "Normal volatility indicates balance.")
    else:
        add("Equity Volatility (VIX)", vix, "negative", 0, "High volatility signals stress.")

    state = "RISK-ON" if score >= 5 else "TRANSITION" if score >= 3 else "RISK-OFF"

    return {
        "state": state,
        "score": score,
        "explanation": "Macro regime derived from real yields, dollar strength and volatility.",
        "parameters": parameters
    }
