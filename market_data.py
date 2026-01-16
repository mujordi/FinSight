"""
FinSight - Market Data Fetcher
Obtains real-time financial data from various sources
"""

import yfinance as yf
import requests
from datetime import datetime
from typing import Dict, Optional

class MarketDataFetcher:
    """Fetches real-time market data from various APIs"""
    
    @staticmethod
    def get_price(symbol: str) -> Optional[float]:
        """Get current price for a symbol using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return round(data['Close'].iloc[-1], 2)
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
        return None
    
    @staticmethod
    def get_change_percent(symbol: str) -> Optional[float]:
        """Get percentage change for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d")
            if len(data) >= 2:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-2]
                change = ((current - previous) / previous) * 100
                return round(change, 2)
        except Exception as e:
            print(f"Error fetching change for {symbol}: {e}")
        return None
    
    @staticmethod
    def get_macro_data() -> Dict[str, any]:
        """Get macro indicators data"""
        data = {}
        
        # US Dollar Index
        dxy_price = MarketDataFetcher.get_price("DX-Y.NYB")
        data['dxy'] = {
            'value': dxy_price or 103.5,
            'change': MarketDataFetcher.get_change_percent("DX-Y.NYB") or 0
        }
        
        # VIX Volatility Index
        vix_price = MarketDataFetcher.get_price("^VIX")
        data['vix'] = {
            'value': vix_price or 15.2,
            'change': MarketDataFetcher.get_change_percent("^VIX") or 0
        }
        
        # 10-Year Treasury Yield (approximate via TLT ETF inverse)
        tlt_price = MarketDataFetcher.get_price("^TNX")
        data['us10y'] = {
            'value': tlt_price or 4.15,
            'change': MarketDataFetcher.get_change_percent("^TNX") or 0
        }
        
        # 2-Year Treasury Yield
        us2y_price = MarketDataFetcher.get_price("^IRX")
        # Convert from percentage to actual rate
        data['us2y'] = {
            'value': (us2y_price / 100) if us2y_price else 4.45,
            'change': MarketDataFetcher.get_change_percent("^IRX") or 0
        }
        
        # Real Yields (approximate: 10Y - Inflation expectations ~2.3%)
        if data['us10y']['value']:
            data['real_yields'] = {
                'value': round(data['us10y']['value'] - 2.3, 2),
                'change': data['us10y']['change']
            }
        else:
            data['real_yields'] = {'value': 1.85, 'change': 0}
        
        # Inflation (using TIP ETF as proxy)
        tip_change = MarketDataFetcher.get_change_percent("TIP")
        data['inflation'] = {
            'value': 2.3,  # Approximate current inflation expectations
            'change': tip_change or 0
        }
        
        # Yield Curve (10Y - 2Y spread)
        spread = data['us10y']['value'] - data['us2y']['value']
        data['yield_curve'] = {
            'value': round(spread, 2),
            'change': 0  # Simplified
        }
        
        return data
    
    @staticmethod
    def get_gold_data() -> Dict[str, any]:
        """Get gold market data"""
        gold_price = MarketDataFetcher.get_price("GC=F")
        gold_change = MarketDataFetcher.get_change_percent("GC=F")
        
        return {
            'gold': {
                'value': gold_price or 2050,
                'change': gold_change or 0
            }
        }
    
    @staticmethod
    def get_equities_data() -> Dict[str, any]:
        """Get equities market data"""
        data = {}
        
        # Nasdaq 100
        ndx_price = MarketDataFetcher.get_price("^NDX")
        data['ndx'] = {
            'value': ndx_price or 16500,
            'change': MarketDataFetcher.get_change_percent("^NDX") or 0
        }
        
        # S&P 500 for liquidity proxy
        spx_price = MarketDataFetcher.get_price("^GSPC")
        data['spx'] = {
            'value': spx_price or 4800,
            'change': MarketDataFetcher.get_change_percent("^GSPC") or 0
        }
        
        # PE Ratio proxy (approximate)
        data['valuations'] = {
            'value': 25.5,  # Approximate current market PE
            'change': 0
        }
        
        return data
    
    @staticmethod
    def get_crypto_data() -> Dict[str, any]:
        """Get crypto market data"""
        data = {}
        
        # Bitcoin
        btc_price = MarketDataFetcher.get_price("BTC-USD")
        data['btc'] = {
            'value': btc_price or 43000,
            'change': MarketDataFetcher.get_change_percent("BTC-USD") or 0
        }
        
        # Ethereum
        eth_price = MarketDataFetcher.get_price("ETH-USD")
        data['eth'] = {
            'value': eth_price or 2250,
            'change': MarketDataFetcher.get_change_percent("ETH-USD") or 0
        }
        
        return data
    
    @staticmethod
    def get_fixed_income_data() -> Dict[str, any]:
        """Get fixed income data"""
        data = {}
        
        # Use macro data for yields
        macro = MarketDataFetcher.get_macro_data()
        data['us10y'] = macro['us10y']
        data['us2y'] = macro['us2y']
        data['yield_curve'] = macro['yield_curve']
        data['inflation'] = macro['inflation']
        
        # TLT ETF
        tlt_price = MarketDataFetcher.get_price("TLT")
        data['tlt'] = {
            'value': tlt_price or 93.5,
            'change': MarketDataFetcher.get_change_percent("TLT") or 0
        }
        
        return data
    
    @staticmethod
    def get_thematic_data() -> Dict[str, any]:
        """Get thematic stocks/ETFs data"""
        data = {}
        
        # Semiconductors ETF
        smh_price = MarketDataFetcher.get_price("SMH")
        data['smh'] = {
            'value': smh_price or 165,
            'change': MarketDataFetcher.get_change_percent("SMH") or 0
        }
        
        # NVIDIA
        nvda_price = MarketDataFetcher.get_price("NVDA")
        data['nvda'] = {
            'value': nvda_price or 495,
            'change': MarketDataFetcher.get_change_percent("NVDA") or 0
        }
        
        # Uranium ETF
        ura_price = MarketDataFetcher.get_price("URA")
        data['ura'] = {
            'value': ura_price or 28.5,
            'change': MarketDataFetcher.get_change_percent("URA") or 0
        }
        
        # Clean Energy ETF
        icln_price = MarketDataFetcher.get_price("ICLN")
        data['icln'] = {
            'value': icln_price or 21.8,
            'change': MarketDataFetcher.get_change_percent("ICLN") or 0
        }
        
        return data
    
    @staticmethod
    def get_growth_data() -> Dict[str, any]:
        """Get growth stocks data"""
        data = {}
        
        # Nasdaq 100
        ndx_price = MarketDataFetcher.get_price("^NDX")
        data['ndx'] = {
            'value': ndx_price or 16500,
            'change': MarketDataFetcher.get_change_percent("^NDX") or 0
        }
        
        # Apple
        aapl_price = MarketDataFetcher.get_price("AAPL")
        data['aapl'] = {
            'value': aapl_price or 185,
            'change': MarketDataFetcher.get_change_percent("AAPL") or 0
        }
        
        # Alphabet
        googl_price = MarketDataFetcher.get_price("GOOGL")
        data['googl'] = {
            'value': googl_price or 141,
            'change': MarketDataFetcher.get_change_percent("GOOGL") or 0
        }
        
        # Microsoft
        msft_price = MarketDataFetcher.get_price("MSFT")
        data['msft'] = {
            'value': msft_price or 375,
            'change': MarketDataFetcher.get_change_percent("MSFT") or 0
        }
        
        return data
    
    @staticmethod
    def get_highbeta_data() -> Dict[str, any]:
        """Get high beta stocks data"""
        data = {}
        
        # MicroStrategy
        mstr_price = MarketDataFetcher.get_price("MSTR")
        data['mstr'] = {
            'value': mstr_price or 485,
            'change': MarketDataFetcher.get_change_percent("MSTR") or 0
        }
        
        # Palantir
        pltr_price = MarketDataFetcher.get_price("PLTR")
        data['pltr'] = {
            'value': pltr_price or 18.5,
            'change': MarketDataFetcher.get_change_percent("PLTR") or 0
        }
        
        # Coinbase
        coin_price = MarketDataFetcher.get_price("COIN")
        data['coin'] = {
            'value': coin_price or 145,
            'change': MarketDataFetcher.get_change_percent("COIN") or 0
        }
        
        # NVIDIA
        nvda_price = MarketDataFetcher.get_price("NVDA")
        data['nvda'] = {
            'value': nvda_price or 495,
            'change': MarketDataFetcher.get_change_percent("NVDA") or 0
        }
        
        return data
    
    @staticmethod
    def get_all_data() -> Dict[str, any]:
        """Get all market data"""
        return {
            'macro': MarketDataFetcher.get_macro_data(),
            'gold': MarketDataFetcher.get_gold_data(),
            'equities': MarketDataFetcher.get_equities_data(),
            'crypto': MarketDataFetcher.get_crypto_data(),
            'fixed_income': MarketDataFetcher.get_fixed_income_data(),
            'thematic': MarketDataFetcher.get_thematic_data(),
            'growth': MarketDataFetcher.get_growth_data(),
            'highbeta': MarketDataFetcher.get_highbeta_data(),
            'last_update': datetime.now().isoformat()
        }

