
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import json

API_KEY = "mujordi"
app = FastAPI()

def check(request):
    if request.query_params.get("key") != API_KEY:
        raise HTTPException(status_code=401)

def load():
    try:
        with open("macro_state.json") as f:
            return json.load(f)
    except:
        return {}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    check(request)
    html = open("templates/index.html").read()
    return html.replace("__DATA__", json.dumps(load()))

@app.get("/state")
def state(request: Request):
    check(request)
    return JSONResponse(load())
