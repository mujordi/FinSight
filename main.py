
from fastapi import FastAPI, Request, HTTPException
from macro_model import macro_model

API_KEY = "canvia_aixo"

app = FastAPI()

@app.get("/macro")
def read_macro(request: Request):
    key = request.query_params.get("key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = {
        "real_yield": 0.7,
        "dxy": 102,
        "vix": 14,
        "yield_curve": 0.2
    }

    return macro_model(data)
