from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from macro_model import macro_model
from data_fetcher import get_real_yield, get_dxy, get_vix, get_curve
from storage import load

API_KEY = "mujordi"

app = FastAPI()

def get_data():
    return {
        "real_yield": get_real_yield(),
        "dxy": get_dxy(),
        "vix": get_vix(),
        "yield_curve": get_curve()
    }

def check_key(request: Request):
    key = request.query_params.get("key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/macro")
def api_macro(request: Request):
    check_key(request)
    return macro_model(get_data())

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    check_key(request)

    result = load()
    if not result:
        result = macro_model(get_data())

    color = {
        "RISC FAVORABLE": "#16a34a",
        "TRANSICIÓ": "#eab308",
        "RISC RESTRICTIU": "#dc2626"
    }[result["macro_state"]]

    return f"""
    <html>
    <head>
      <title>FinSight</title>
    </head>
    <body style="background:#0f172a;color:white;font-family:Arial;padding:40px">
      <div style="background:#020617;padding:30px;border-radius:12px;max-width:600px">
        <h1 style="color:{color}">{result["macro_state"]}</h1>
        <p>Data: {result["date"]}</p>
        <p>Score: {result["score"]}</p>
        <h3>Indicadors</h3>
        <ul>
          <li>Tipus reals: {result["details"]["real_yield"]}</li>
          <li>DXY: {result["details"]["dxy"]}</li>
          <li>VIX: {result["details"]["vix"]}</li>
          <li>Corba: {result["details"]["curve"]}</li>
        </ul>
      </div>
    </body>
    </html>
    """
