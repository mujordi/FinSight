import requests
import os

FRED_KEY = os.getenv("FRED_API_KEY")

def safe_float(x, default=0):
    try:
        return float(x)
    except:
        return default

def get_fred(series):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series,
        "api_key": FRED_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if "observations" not in data:
            print("FRED error:", data)
            return 0

        return safe_float(data["observations"][0]["value"])
    except Exception as e:
        print("FRED exception:", e)
        return 0

def get_real_yield():
    return get_fred("DFII10")

def get_curve():
    return get_fred("DGS10") - get_fred("DGS2")

def get_yahoo(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        r = requests.get(url, timeout=10)
        return safe_float(r.json()["quoteResponse"]["result"][0]["regularMarketPrice"])
    except Exception as e:
        print("Yahoo error:", e)
        return 0

def get_dxy():
    return get_yahoo("DX-Y.NYB")

def get_vix():
    return get_yahoo("^VIX")

