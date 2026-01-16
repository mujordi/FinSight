
from fastapi import FastAPI, Request, Response, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import date
from jinja2 import Environment, FileSystemLoader
from auth import AuthManager
from market_data_fast import FastMarketData
from portfolio_manager import PortfolioManager
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

env = Environment(loader=FileSystemLoader("templates"))

# Initialize managers
auth_manager = AuthManager()
fast_data = FastMarketData()
portfolio_manager = PortfolioManager()

def get_market_data():
    """Lazy initialization of REAL market data fetcher (slow)"""
    from market_data import MarketDataFetcher
    return MarketDataFetcher()

def get_model_logic():
    """Lazy initialization of model logic"""
    from model_logic import ModelLogic
    return ModelLogic()

# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

def check_auth(auth_token: Optional[str]) -> bool:
    """Helper function to check authentication"""
    return auth_manager.validate_session(auth_token)

@app.get("/login", response_class=HTMLResponse)
def login_page():
    """Display login page"""
    template = env.get_template("login.html")
    return template.render()

@app.post("/api/login")
async def login(request: LoginRequest):
    """Handle login request"""
    token = auth_manager.authenticate(request.username, request.password)
    
    if token:
        # Create response with cookie
        json_response = JSONResponse(content={
            "success": True,
            "token": token,
            "message": "Login successful"
        })
        json_response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=86400,  # 24 hours
            samesite="lax"
        )
        return json_response
    else:
        return JSONResponse(
            content={
                "success": False,
                "message": "Invalid username or password"
            },
            status_code=401
        )

@app.get("/api/logout")
async def logout(auth_token: Optional[str] = Cookie(None)):
    """Handle logout request"""
    if auth_token:
        auth_manager.logout(auth_token)
    
    redirect_response = RedirectResponse(url="/login")
    redirect_response.delete_cookie("auth_token")
    return redirect_response

@app.get("/", response_class=HTMLResponse)
def home(auth_token: Optional[str] = Cookie(None)):
    """Main application page - requires authentication"""
    if not check_auth(auth_token):
        return RedirectResponse(url="/login")
    
    username = auth_manager.get_username(auth_token)
    template = env.get_template("base.html")
    return template.render(
        today=date.today().isoformat(),
        username=username
    )

@app.get("/api/market-data/all")
async def get_all_market_data(auth_token: Optional[str] = Cookie(None)):
    """Get FAST mock market data for instant loading"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        # Use fast mock data for instant response
        data = fast_data.get_all_data()
        # Calculate dynamic signals based on current data
        model_logic = get_model_logic()
        signals = model_logic.calculate_all_signals(data)
        data['signals'] = signals
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/all/real")
async def get_all_market_data_real(auth_token: Optional[str] = Cookie(None)):
    """Get REAL market data (slower, from yfinance)"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        # Use real market data (slower)
        market_data = get_market_data()
        data = market_data.get_all_data()
        # Calculate dynamic signals based on current data
        model_logic = get_model_logic()
        signals = model_logic.calculate_all_signals(data)
        data['signals'] = signals
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/macro")
async def get_macro_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get macro indicators data - FAST"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_macro_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/gold")
async def get_gold_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get gold market data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_gold_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/equities")
async def get_equities_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get equities market data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_equities_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/crypto")
async def get_crypto_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get crypto market data - FAST"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_crypto_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/fixed-income")
async def get_fixed_income_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get fixed income data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_fixed_income_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/thematic")
async def get_thematic_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get thematic stocks data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_thematic_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/growth")
async def get_growth_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get growth stocks data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_growth_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/market-data/highbeta")
async def get_highbeta_data_endpoint(auth_token: Optional[str] = Cookie(None)):
    """Get high beta stocks data"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    try:
        data = fast_data.get_highbeta_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# ===== PORTFOLIO ENDPOINTS =====

class AddProductRequest(BaseModel):
    name: str
    ticker: str
    percentage: float

@app.get("/api/portfolio")
async def get_portfolio(auth_token: Optional[str] = Cookie(None)):
    '''Get user portfolio'''
    if not check_auth(auth_token):
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    username = auth_manager.get_username(auth_token)
    portfolio = portfolio_manager.load_portfolio(username)
    return JSONResponse(content=portfolio)

@app.post("/api/portfolio/add")
async def add_product(request: AddProductRequest, auth_token: Optional[str] = Cookie(None)):
    '''Add product to portfolio'''
    if not check_auth(auth_token):
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    username = auth_manager.get_username(auth_token)
    product = portfolio_manager.add_product(
        username, 
        request.name, 
        request.ticker, 
        request.percentage
    )
    return JSONResponse(content=product)

@app.delete("/api/portfolio/remove/{product_id}")
async def remove_product(product_id: str, auth_token: Optional[str] = Cookie(None)):
    '''Remove product from portfolio'''
    if not check_auth(auth_token):
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    username = auth_manager.get_username(auth_token)
    success = portfolio_manager.remove_product(username, product_id)
    return JSONResponse(content={"success": success})

@app.post("/api/portfolio/import-csv")
async def import_csv(file: UploadFile = File(...), auth_token: Optional[str] = Cookie(None)):
    '''Import portfolio from CSV'''
    if not check_auth(auth_token):
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
    
    username = auth_manager.get_username(auth_token)
    content = await file.read()
    csv_content = content.decode('utf-8')
    
    result = portfolio_manager.import_from_csv(username, csv_content)
    return JSONResponse(content=result)
