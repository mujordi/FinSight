
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json

app=FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/",response_class=HTMLResponse)
def home():
    d=json.load(open("state.json"))
    html=open("templates/index.html",encoding="utf-8").read()
    return html.replace("__DATA__",json.dumps(d))
