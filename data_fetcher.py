
import requests, os, csv, io
from dotenv import load_dotenv
load_dotenv()
FRED=os.getenv("FRED_API_KEY")

def fred(series,limit=36):
    r=requests.get("https://api.stlouisfed.org/fred/series/observations",params={
        "series_id":series,"api_key":FRED,"file_type":"json","sort_order":"desc","limit":limit},timeout=10)
    j=r.json()
    return [float(x["value"]) for x in j.get("observations",[]) if x["value"]!="."]

def snapshot():
    return {
        "real_yield": fred("DFII10",1)[0],
        "inflation": (fred("CPIAUCSL",13)[0]/fred("CPIAUCSL",13)[-1]-1)*100,
        "curve": fred("DGS10",1)[0]-fred("DGS2",1)[0],
        "dxy": fred("DTWEXBGS",1)[0],
        "vix": float(list(csv.DictReader(io.StringIO(
            requests.get("https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv").text)))[-1]["CLOSE"])
    }

def series():
    return {
        "real_yield": fred("DFII10")[::-1],
        "dollar": fred("DTWEXBGS")[::-1]
    }
