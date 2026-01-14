
def nasdaq_model(macro):
    score = 0
    parameters = []

    for p in macro["parameters"]:
        impact = 0
        if p["parameter"] == "Real Yield (10Y)" and p["signal"] != "negative":
            impact = 2
        if p["parameter"] == "Equity Volatility (VIX)" and p["signal"] == "positive":
            impact = 2
        if p["parameter"] == "US Dollar Index (DXY)" and p["signal"] != "negative":
            impact = 1
        score += impact

        parameters.append({
            "parameter": p["parameter"],
            "real_value": p["real_value"],
            "signal": p["signal"],
            "impact": impact,
            "explanation": "Macro variable affecting growth equity valuations."
        })

    state = "BULLISH" if score >= 4 else "NEUTRAL" if score >= 2 else "UNFAVORABLE"

    return {
        "state": state,
        "score": score,
        "explanation": "Nasdaq performance depends on rates, volatility and liquidity.",
        "parameters": parameters
    }
