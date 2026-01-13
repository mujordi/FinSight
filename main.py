from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from macro_model import macro_model
from data_fetcher import get_real_yield,get_dxy,get_vix,get_curve
from storage import load

app=FastAPI()

def get_data(): return {'real_yield':get_real_yield(),'dxy':get_dxy(),'vix':get_vix(),'yield_curve':get_curve()}

@app.get('/macro')
def api(): return macro_model(get_data())

@app.get('/',response_class=HTMLResponse)
def dash():
    r=load() or macro_model(get_data())
    return f"<html><body style='background:#0f172a;color:white'><h1>{r['macro_state']}</h1><p>{r}</p></body></html>"
