from fastapi import FastAPI, Request, HTTPException
from macro_model import macro_model

API_KEY = "mujordi"

app = FastAPI()

def get_data():
    return {
        "real_yield": 0.7,
        "dxy": 102,
        "vix": 14,
        "yield_curve": 0.2
    }

@app.get("/macro")
def read_macro(request: Request):
    key = request.query_params.get("key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return macro_model(get_data())

@app.get("/")
def dashboard():
    result = macro_model(get_data())

    state = result["macro_state"]
    color = {
        "RISC FAVORABLE": "#16a34a",
        "TRANSICIÓ": "#eab308",
        "RISC RESTRICTIU": "#dc2626"
    }[state]

    html = f"""
    <html>
    <head>
        <title>FinSight – Macro Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                padding: 40px;
            }}
            .box {{
                background: #020617;
                padding: 30px;
                border-radius: 12px;
                max-width: 600px;
            }}
            .state {{
                font-size: 48px;
                font-weight: bold;
                color: {color};
            }}
            .item {{
                margin-top: 12px;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="state">{state}</div>
            <div class="item">Data: {result["date"]}</div>
            <div class="item">Score: {result["score"]}</div>

            <h3>Indicadors</h3>
            <div class="item">Tipus reals: {result["details"]["real_yield"]}</div>
            <div class="item">Dòlar (DXY): {result["details"]["dxy"]}</div>
            <div class="item">Volatilitat: {result["details"]["vix"]}</div>
            <div class="item">Corba: {result["details"]["curve"]}</div>
        </div>
    </body>
    </html>
    """
    return html

