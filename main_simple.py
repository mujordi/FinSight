"""
Simplified version for testing authentication without market data
"""
from fastapi import FastAPI, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import date
from jinja2 import Environment, FileSystemLoader
from auth import AuthManager
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

env = Environment(loader=FileSystemLoader("templates"))

# Initialize auth manager only
auth_manager = AuthManager()

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
async def login(request: LoginRequest, response: Response):
    """Handle login request"""
    token = auth_manager.authenticate(request.username, request.password)
    
    if token:
        # Set cookie with token
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            max_age=86400,  # 24 hours
            samesite="lax"
        )
        return JSONResponse(content={
            "success": True,
            "token": token,
            "message": "Login successful"
        })
    else:
        return JSONResponse(
            content={
                "success": False,
                "message": "Invalid username or password"
            },
            status_code=401
        )

@app.get("/api/logout")
async def logout(response: Response, auth_token: Optional[str] = Cookie(None)):
    """Handle logout request"""
    if auth_token:
        auth_manager.logout(auth_token)
    
    response.delete_cookie("auth_token")
    return RedirectResponse(url="/login")

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
    """Get all market data - MOCK VERSION"""
    if not check_auth(auth_token):
        return JSONResponse(
            content={"error": "Unauthorized"},
            status_code=401
        )
    
    # Return mock data for testing
    return JSONResponse(content={
        "macro": {"dxy": {"value": 103.5, "change": 0.5}},
        "crypto": {"btc": {"value": 45000, "change": 2.3}},
        "signals": {}
    })

