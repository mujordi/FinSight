"""
Portfolio Manager - Manages user portfolios
Each user has their own portfolio stored in JSON
"""
import json
import os
import uuid
from typing import Dict, List, Optional
from pathlib import Path
import yfinance as yf

class PortfolioManager:
    """Manages user portfolios"""
    
    def __init__(self, storage_dir: str = "portfolios"):
        self.storage_dir = storage_dir
        Path(storage_dir).mkdir(exist_ok=True)
    
    def _get_portfolio_path(self, username: str) -> str:
        """Get path to user's portfolio file"""
        return os.path.join(self.storage_dir, f"{username}.json")
    
    def load_portfolio(self, username: str) -> Dict:
        """Load user's portfolio"""
        path = self._get_portfolio_path(username)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"username": username, "products": []}
    
    def save_portfolio(self, username: str, portfolio: Dict):
        """Save user's portfolio"""
        path = self._get_portfolio_path(username)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, indent=2, ensure_ascii=False)
    
    def add_product(self, username: str, name: str, ticker: str, percentage: float) -> Dict:
        """Add product to portfolio with auto-classification"""
        portfolio = self.load_portfolio(username)
        
        # Auto-classify product
        product_type, model = self.classify_product(name, ticker)
        
        product = {
            "id": str(uuid.uuid4()),
            "name": name.strip(),
            "ticker": ticker.strip().upper() if ticker else "",
            "type": product_type,
            "model": model,
            "percentage": round(percentage, 2)
        }
        
        portfolio["products"].append(product)
        self.save_portfolio(username, portfolio)
        
        return product
    
    def remove_product(self, username: str, product_id: str) -> bool:
        """Remove product from portfolio"""
        portfolio = self.load_portfolio(username)
        original_len = len(portfolio["products"])
        portfolio["products"] = [p for p in portfolio["products"] if p["id"] != product_id]
        
        if len(portfolio["products"]) < original_len:
            self.save_portfolio(username, portfolio)
            return True
        return False
    
    def update_product(self, username: str, product_id: str, updates: Dict) -> bool:
        """Update product in portfolio"""
        portfolio = self.load_portfolio(username)
        
        for product in portfolio["products"]:
            if product["id"] == product_id:
                product.update(updates)
                self.save_portfolio(username, portfolio)
                return True
        return False
    
    def get_distribution(self, username: str) -> Dict:
        """Get portfolio distribution by model"""
        portfolio = self.load_portfolio(username)
        distribution = {}
        
        for product in portfolio["products"]:
            model = product["model"]
            distribution[model] = distribution.get(model, 0) + product["percentage"]
        
        return distribution
    
    def classify_product(self, name: str, ticker: str) -> tuple:
        """Classify product into type and model"""
        name_lower = name.lower()
        ticker_upper = ticker.upper() if ticker else ""
        
        # Determine type (more specific checks first)
        product_type = "Unknown"
        
        # Cash
        if any(k in name_lower for k in ['cash', 'cuenta', 'compta', 'remunerada']):
            product_type = "Cash"
        # ETF
        elif any(k in name_lower for k in ['etf', 'vaneck', 'ishares', 'spdr', 'vanguard etf']):
            product_type = "ETF"
        # Funds (check multiple keywords)
        elif any(k in name_lower for k in [
            'fund', 'fondo', 'fi ', ' fi', 'f.i', 'icav', 'sicav',
            'bond', 'bonds', 'obligaciones', 'renta fija',
            'gestion boutique', 'gestión', 'gestivalue',
            'heptagon', 'dws invest', 'jupiter', 'kopernik',
            'wcm select', 'b&h', 'equity fund', 'global growth'
        ]):
            product_type = "Fund"
        # RSU/ESPP
        elif any(k in name_lower for k in ['rsu', 'espp', 'stock option']):
            product_type = "Stock (RSU/ESPP)"
        # Stock (only if has ticker and not identified as other type)
        elif ticker_upper and len(ticker_upper) <= 5:
            product_type = "Stock"
        else:
            # If no ticker and not identified, probably a fund or other product
            product_type = "Other"
        
        # Classify into model
        model = self._classify_to_model(name_lower, ticker_upper)
        
        return product_type, model
    
    def _classify_to_model(self, name: str, ticker: str) -> str:
        """Classify product to one of the 8 models"""
        
        # GOLD
        if any(k in name for k in ['gold', 'oro', 'silver', 'plata', 'precious', 'metales preciosos']):
            return "Gold"
        
        # CRYPTO
        if any(k in name for k in ['bitcoin', 'crypto', 'blockchain', 'btc', 'eth', 'ethereum']):
            return "Crypto"
        
        # THEMATIC (Semiconductors, AI, Uranium, Tech themes)
        if any(k in name for k in [
            'semiconductor', 'chip', 'quantum', 'uranium', 'nuclear',
            'nvidia', 'nvda', 'amd', 'intel', 'broadcom', 'synopsys',
            'palantir', 'pltr', 'smh'
        ]):
            return "Thematic"
        
        # FIXED INCOME
        if any(k in name for k in ['bond', 'fixed', 'treasury', 'yield', 'renta fija', 'obligaciones']):
            return "Fixed Income"
        
        # HIGH BETA (Leveraged, 3x, inverse)
        if any(k in name for k in ['3x', 'leveraged', 'sqqq', 'tqqq', 'spxl', 'upro', 'inverse']):
            return "High Beta"
        
        # GROWTH/QUALITY (Big tech, mega caps)
        if any(k in ticker or k in name for k in [
            'meta', 'googl', 'alphabet', 'aapl', 'apple', 'msft', 'microsoft',
            'tsla', 'tesla', 'arkk', 'growth', 'quality'
        ]):
            return "Growth"
        
        # MACRO (Cash, commodities, DXY, etc.)
        if any(k in name for k in ['cash', 'money market', 'cuenta', 'compta', 'dxy', 'dollar']):
            return "Macro"
        
        # Default: EQUITIES
        return "Equities"
    
    def import_from_csv(self, username: str, csv_content: str) -> Dict:
        """Import products from CSV content"""
        import csv
        from io import StringIO
        
        portfolio = self.load_portfolio(username)
        added = 0
        errors = []
        
        try:
            reader = csv.DictReader(StringIO(csv_content))
            
            for row in reader:
                try:
                    name = row.get('name') or row.get('producto') or row.get('product', '')
                    ticker = row.get('ticker', '')
                    percentage = float(row.get('percentage') or row.get('%') or 0)
                    
                    if name and percentage > 0:
                        self.add_product(username, name, ticker, percentage)
                        added += 1
                except Exception as e:
                    errors.append(f"Error in row {row}: {str(e)}")
            
            return {
                "success": True,
                "added": added,
                "errors": errors
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

