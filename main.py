
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json
app=FastAPI()
@app.get("/",response_class=HTMLResponse)
def home():
    return open("templates/index.html").read().replace("__DATA__",json.dumps(json.load(open("state.json"))))
