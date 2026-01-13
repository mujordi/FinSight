
import datetime

def score_real_yield(value):
    if value < 0:
        return 0, "favorable"
    elif value < 1.5:
        return 1, "neutral"
    else:
        return 2, "restrictiu"

def score_dxy(value):
    if value < 100:
        return 0, "favorable"
    elif value < 105:
        return 1, "neutral"
    else:
        return 2, "alerta"

def score_vix(value):
    if value < 15:
        return 0, "calma"
    elif value < 20:
        return 1, "normal"
    else:
        return 2, "estrès"

def score_curve(value):
    if value > 0:
        return 0, "normal"
    elif value > -0.5:
        return 1, "lleu inversió"
    else:
        return 2, "inversió profunda"

def macro_model(data):
    score = 0
    details = {}

    s, d = score_real_yield(data["real_yield"])
    score += s * 2
    details["real_yield"] = d

    s, d = score_dxy(data["dxy"])
    score += s
    details["dxy"] = d

    s, d = score_vix(data["vix"])
    score += s
    details["vix"] = d

    s, d = score_curve(data["yield_curve"])
    score += s
    details["curve"] = d

    if score <= 2:
        state = "RISC FAVORABLE"
    elif score <= 4:
        state = "TRANSICIÓ"
    else:
        state = "RISC RESTRICTIU"

    return {
        "date": datetime.date.today().isoformat(),
        "macro_state": state,
        "score": score,
        "details": details
    }
