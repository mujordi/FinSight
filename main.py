from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from storage import load

API_KEY = "mujordi"

app = FastAPI()

def check_key(request: Request):
    if request.query_params.get("key") != API_KEY:
        raise HTTPException(status_code=401)

@app.get("/macro")
def api_macro(request: Request):
    check_key(request)
    data = load()
    if not data:
        return {"status": "No data yet. Cron has not run."}
    return data

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    check_key(request)
    data = load()
    if not data:
        return "<h1>No data yet – cron not run</h1>"

    color = {
        "RISC FAVORABLE": "#16a34a",
        "TRANSICIÓ": "#eab308",
        "RISC RESTRICTIU": "#dc2626"
    }[data["macro_state"]]

    return f"""
    <html>
    <body style="background:#0f172a;color:white;font-family:Arial;padding:40px">
    <div style="background:#020617;padding:30px;border-radius:12px;max-width:600px">
      <h1 style="color:{color}">{data["macro_state"]}</h1>
      <p>Date: {data["date"]}</p>
      <p>Score: {data["score"]}</p>
      <ul>
        <li>Real Yield: {data["details"]["real_yield"]}</li>
        <li>DXY: {data["details"]["dxy"]}</li>
        <li>VIX: {data["details"]["vix"]}</li>
        <li>Curve: {data["details"]["curve"]}</li>
      </ul>
    </div>
    </body>
    </html>
    """


