"""
FinSight - Fast Market Data with Mock Data
Returns instant mock data for quick page loads
"""
from typing import Dict
import random

class FastMarketData:
    """Returns fast mock data for instant page loads"""
    
    @staticmethod
    def get_mock_value(base: float, variance: float = 0.05) -> float:
        """Generate realistic mock value with small variance"""
        return round(base * (1 + random.uniform(-variance, variance)), 2)
    
    @staticmethod
    def get_mock_change() -> float:
        """Generate realistic mock change percentage"""
        return round(random.uniform(-3, 3), 2)
    
    @staticmethod
    def get_macro_data() -> Dict:
        """Get instant mock macro data"""
        return {
            'dxy': {'value': FastMarketData.get_mock_value(103.5), 'change': FastMarketData.get_mock_change()},
            'vix': {'value': FastMarketData.get_mock_value(15.2), 'change': FastMarketData.get_mock_change()},
            'us10y': {'value': FastMarketData.get_mock_value(4.15), 'change': FastMarketData.get_mock_change()},
            'us2y': {'value': FastMarketData.get_mock_value(4.45), 'change': FastMarketData.get_mock_change()},
            'yield_curve': {'value': FastMarketData.get_mock_value(-0.30), 'change': FastMarketData.get_mock_change()},
            'real_yields': {'value': FastMarketData.get_mock_value(1.85), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_gold_data() -> Dict:
        """Get instant mock gold data"""
        return {
            'gold': {'value': FastMarketData.get_mock_value(2050), 'change': FastMarketData.get_mock_change()},
            'real_yields': {'value': FastMarketData.get_mock_value(1.85), 'change': FastMarketData.get_mock_change()},
            'dxy': {'value': FastMarketData.get_mock_value(103.5), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_crypto_data() -> Dict:
        """Get instant mock crypto data"""
        return {
            'btc': {'value': FastMarketData.get_mock_value(45000), 'change': FastMarketData.get_mock_change()},
            'eth': {'value': FastMarketData.get_mock_value(2400), 'change': FastMarketData.get_mock_change()},
            'sol': {'value': FastMarketData.get_mock_value(105), 'change': FastMarketData.get_mock_change()},
            'total_mcap': {'value': FastMarketData.get_mock_value(1.7, 0.1), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_equities_data() -> Dict:
        """Get instant mock equities data"""
        return {
            'sp500': {'value': FastMarketData.get_mock_value(4800), 'change': FastMarketData.get_mock_change()},
            'nasdaq': {'value': FastMarketData.get_mock_value(15000), 'change': FastMarketData.get_mock_change()},
            'pe_ratio': {'value': FastMarketData.get_mock_value(22.5), 'change': FastMarketData.get_mock_change()},
            'earnings_growth': {'value': FastMarketData.get_mock_value(8.5), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_fixed_income_data() -> Dict:
        """Get instant mock fixed income data"""
        return {
            'us10y': {'value': FastMarketData.get_mock_value(4.15), 'change': FastMarketData.get_mock_change()},
            'us2y': {'value': FastMarketData.get_mock_value(4.45), 'change': FastMarketData.get_mock_change()},
            'yield_curve': {'value': FastMarketData.get_mock_value(-0.30), 'change': FastMarketData.get_mock_change()},
            'tlt': {'value': FastMarketData.get_mock_value(95), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_thematic_data() -> Dict:
        """Get instant mock thematic data"""
        return {
            'smh': {'value': FastMarketData.get_mock_value(180), 'change': FastMarketData.get_mock_change()},
            'nvda': {'value': FastMarketData.get_mock_value(500), 'change': FastMarketData.get_mock_change()},
            'ura': {'value': FastMarketData.get_mock_value(28), 'change': FastMarketData.get_mock_change()},
            'icln': {'value': FastMarketData.get_mock_value(22), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_growth_data() -> Dict:
        """Get instant mock growth data"""
        return {
            'arkk': {'value': FastMarketData.get_mock_value(45), 'change': FastMarketData.get_mock_change()},
            'qqq': {'value': FastMarketData.get_mock_value(380), 'change': FastMarketData.get_mock_change()},
            'tesla': {'value': FastMarketData.get_mock_value(250), 'change': FastMarketData.get_mock_change()},
            'meta': {'value': FastMarketData.get_mock_value(350), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_highbeta_data() -> Dict:
        """Get instant mock high beta data"""
        return {
            'sqqq': {'value': FastMarketData.get_mock_value(12), 'change': FastMarketData.get_mock_change()},
            'tqqq': {'value': FastMarketData.get_mock_value(55), 'change': FastMarketData.get_mock_change()},
            'spxl': {'value': FastMarketData.get_mock_value(120), 'change': FastMarketData.get_mock_change()},
            'upro': {'value': FastMarketData.get_mock_value(65), 'change': FastMarketData.get_mock_change()},
        }
    
    @staticmethod
    def get_all_data() -> Dict:
        """Get all mock data instantly"""
        return {
            'macro': FastMarketData.get_macro_data(),
            'gold': FastMarketData.get_gold_data(),
            'crypto': FastMarketData.get_crypto_data(),
            'equities': FastMarketData.get_equities_data(),
            'fixedincome': FastMarketData.get_fixed_income_data(),
            'thematic': FastMarketData.get_thematic_data(),
            'growth': FastMarketData.get_growth_data(),
            'highbeta': FastMarketData.get_highbeta_data(),
        }



