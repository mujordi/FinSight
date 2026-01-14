
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import json

API_KEY="mujordi"
app=FastAPI()

def check(request):
    if request.query_params.get("key")!=API_KEY:
        raise HTTPException(status_code=401)

def load():
    try:
        with open("macro_state.json") as f:
            return json.load(f)
    except:
        return None

@app.get("/macro")
def macro(request:Request):
    check(request)
    return JSONResponse(load())

@app.get("/", response_class=HTMLResponse)
def home(request:Request):
    check(request)
    data=load() or {}
    html=open("templates/index.html").read()
    return html.replace("__DATA__", json.dumps(data))
