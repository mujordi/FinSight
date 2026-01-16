
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import date
from jinja2 import Environment, FileSystemLoader
from market_data import MarketDataFetcher
from model_logic import ModelLogic

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

env = Environment(loader=FileSystemLoader("templates"))

# Initialize market data fetcher and model logic
market_data = MarketDataFetcher()
model_logic = ModelLogic()

@app.get("/", response_class=HTMLResponse)
def home():
    template = env.get_template("base.html")
    return template.render(today=date.today().isoformat())

@app.get("/api/market-data/all")
async def get_all_market_data():
    """Get all market data for all tabs with dynamic signals"""
    try:
        data = market_data.get_all_data()
        # Calculate dynamic signals based on current data
        signals = model_logic.calculate_all_signals(data)
        data['signals'] = signals
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/macro")
async def get_macro_data():
    """Get macro indicators data"""
    try:
        data = market_data.get_macro_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/gold")
async def get_gold_data():
    """Get gold market data"""
    try:
        data = market_data.get_gold_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/equities")
async def get_equities_data():
    """Get equities market data"""
    try:
        data = market_data.get_equities_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/crypto")
async def get_crypto_data():
    """Get crypto market data"""
    try:
        data = market_data.get_crypto_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/fixed-income")
async def get_fixed_income_data():
    """Get fixed income data"""
    try:
        data = market_data.get_fixed_income_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/thematic")
async def get_thematic_data():
    """Get thematic stocks data"""
    try:
        data = market_data.get_thematic_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/growth")
async def get_growth_data():
    """Get growth stocks data"""
    try:
        data = market_data.get_growth_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/highbeta")
async def get_highbeta_data():
    """Get high beta stocks data"""
    try:
        data = market_data.get_highbeta_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
