"""
FinSight - Model Logic
Dynamic calculation of signals, weights, and explanations based on market data
"""

from typing import Dict, Literal

Signal = Literal["positive", "neutral", "negative"]
Weight = Literal["high", "medium", "low"]

class ModelLogic:
    """Calculates dynamic signals based on market data"""
    
    @staticmethod
    def calculate_macro_signals(data: Dict) -> Dict:
        """Calculate macro model signals"""
        signals = {}
        
        # Real Yields
        real_yields = data.get('real_yields', {}).get('value', 1.85)
        if real_yields > 2.5:
            signals['real_yields'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Very high real yields pressure valuations significantly'
            }
        elif real_yields > 1.5:
            signals['real_yields'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'High real yields pressure valuations'
            }
        elif real_yields > 0.5:
            signals['real_yields'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Moderate real yields neutral for risk assets'
            }
        else:
            signals['real_yields'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Low/negative real yields support valuations'
            }
        
        # Inflation
        inflation = data.get('inflation', {}).get('value', 2.3)
        if inflation > 4.0:
            signals['inflation'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'High inflation erodes real returns'
            }
        elif inflation > 3.0:
            signals['inflation'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Elevated inflation, monitoring needed'
            }
        elif inflation > 1.5:
            signals['inflation'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Inflation near target, disinflation ongoing'
            }
        else:
            signals['inflation'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Low inflation supports loose monetary policy'
            }
        
        # Yield Curve (10Y - 2Y)
        yield_curve = data.get('yield_curve', {}).get('value', -0.3)
        if yield_curve > 0.5:
            signals['yield_curve'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Steep curve signals strong growth ahead'
            }
        elif yield_curve > 0:
            signals['yield_curve'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Curve re-steepening, recession risk fading'
            }
        elif yield_curve > -0.5:
            signals['yield_curve'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Flat curve, uncertain growth outlook'
            }
        else:
            signals['yield_curve'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Deeply inverted curve signals recession risk'
            }
        
        # Dollar (DXY)
        dxy = data.get('dxy', {}).get('value', 103.5)
        dxy_change = data.get('dxy', {}).get('change', 0)
        if dxy > 110 or dxy_change > 1:
            signals['dxy'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Strong dollar headwind for risk assets'
            }
        elif dxy > 105 or dxy_change > 0.5:
            signals['dxy'] = {
                'signal': 'neutral',
                'weight': 'high',
                'explanation': 'Dollar elevated, monitoring needed'
            }
        elif dxy_change < -0.5:
            signals['dxy'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Weakening dollar supports risk assets'
            }
        else:
            signals['dxy'] = {
                'signal': 'neutral',
                'weight': 'high',
                'explanation': 'Dollar stable'
            }
        
        # VIX
        vix = data.get('vix', {}).get('value', 15.2)
        if vix < 15:
            signals['vix'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Very low volatility, strong risk appetite'
            }
        elif vix < 20:
            signals['vix'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Low volatility supports risk-on'
            }
        elif vix < 30:
            signals['vix'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Elevated volatility, caution warranted'
            }
        else:
            signals['vix'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'High fear, risk-off environment'
            }
        
        return signals
    
    @staticmethod
    def calculate_crypto_signals(data: Dict, macro_data: Dict) -> Dict:
        """Calculate crypto model signals"""
        signals = {}
        
        # Bitcoin
        btc = data.get('btc', {}).get('value', 43000)
        btc_change = data.get('btc', {}).get('change', 0)
        if btc > 60000:
            signals['btc'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Bitcoin at strong levels, bull market'
            }
        elif btc > 40000:
            signals['btc'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Bitcoin healthy, uptrend intact'
            }
        elif btc > 30000:
            signals['btc'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Bitcoin consolidating'
            }
        else:
            signals['btc'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Bitcoin weak, bear market conditions'
            }
        
        # Ethereum
        eth = data.get('eth', {}).get('value', 2250)
        if eth > 3000:
            signals['eth'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Ethereum strong, DeFi momentum'
            }
        elif eth > 2000:
            signals['eth'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Ethereum healthy range'
            }
        elif eth > 1500:
            signals['eth'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Ethereum consolidating'
            }
        else:
            signals['eth'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Ethereum under pressure'
            }
        
        # Risk Appetite (VIX from macro)
        vix = macro_data.get('vix', {}).get('value', 15.2)
        if vix < 20:
            signals['risk_appetite'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Low volatility favors risk assets like crypto'
            }
        else:
            signals['risk_appetite'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'High volatility pressures speculative assets'
            }
        
        # USD (DXY from macro)
        dxy_change = macro_data.get('dxy', {}).get('change', 0)
        if dxy_change < -0.5:
            signals['usd_trend'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Weakening dollar supports crypto'
            }
        elif dxy_change > 0.5:
            signals['usd_trend'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Strengthening dollar headwind for crypto'
            }
        else:
            signals['usd_trend'] = {
                'signal': 'neutral',
                'weight': 'high',
                'explanation': 'Dollar stable, neutral for crypto'
            }
        
        return signals
    
    @staticmethod
    def calculate_equities_signals(data: Dict) -> Dict:
        """Calculate equities model signals"""
        signals = {}
        
        # Nasdaq 100
        ndx = data.get('ndx', {}).get('value', 16500)
        ndx_change = data.get('ndx', {}).get('change', 0)
        if ndx_change > 1:
            signals['ndx'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Strong momentum, tech leadership'
            }
        elif ndx_change > 0:
            signals['ndx'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Positive trend continues'
            }
        elif ndx_change > -1:
            signals['ndx'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Consolidation phase'
            }
        else:
            signals['ndx'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Weakness in tech leadership'
            }
        
        # S&P 500
        spx_change = data.get('spx', {}).get('change', 0)
        if spx_change > 0.5:
            signals['spx'] = {
                'signal': 'positive',
                'weight': 'medium',
                'explanation': 'Broad market strength'
            }
        elif spx_change > -0.5:
            signals['spx'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Mixed breadth'
            }
        else:
            signals['spx'] = {
                'signal': 'negative',
                'weight': 'medium',
                'explanation': 'Broad market weakness'
            }
        
        # Valuations (P/E)
        pe_ratio = data.get('valuations', {}).get('value', 25.5)
        if pe_ratio > 28:
            signals['valuations'] = {
                'signal': 'negative',
                'weight': 'high',
                'explanation': 'Valuations very stretched, bubble risk'
            }
        elif pe_ratio > 23:
            signals['valuations'] = {
                'signal': 'negative',
                'weight': 'medium',
                'explanation': 'Valuations elevated above historical avg'
            }
        elif pe_ratio > 18:
            signals['valuations'] = {
                'signal': 'neutral',
                'weight': 'medium',
                'explanation': 'Valuations fair, near historical average'
            }
        else:
            signals['valuations'] = {
                'signal': 'positive',
                'weight': 'high',
                'explanation': 'Valuations attractive, value opportunity'
            }
        
        return signals
    
    @staticmethod
    def calculate_growth_signals(data: Dict) -> Dict:
        """Calculate growth stocks signals"""
        signals = {}
        
        stocks = ['ndx', 'aapl', 'googl', 'msft']
        for stock in stocks:
            stock_data = data.get(stock, {})
            change = stock_data.get('change', 0)
            value = stock_data.get('value', 0)
            
            if change > 2:
                signals[stock] = {
                    'signal': 'positive',
                    'weight': 'high',
                    'explanation': 'Strong momentum, outperforming'
                }
            elif change > 0:
                signals[stock] = {
                    'signal': 'positive',
                    'weight': 'high',
                    'explanation': 'Positive trend, quality leadership'
                }
            elif change > -2:
                signals[stock] = {
                    'signal': 'neutral',
                    'weight': 'medium',
                    'explanation': 'Consolidating, watching for direction'
                }
            else:
                signals[stock] = {
                    'signal': 'negative',
                    'weight': 'medium',
                    'explanation': 'Under pressure, monitoring support'
                }
        
        return signals
    
    @staticmethod
    def calculate_highbeta_signals(data: Dict) -> Dict:
        """Calculate high beta stocks signals"""
        signals = {}
        
        stocks = ['mstr', 'pltr', 'coin', 'nvda']
        for stock in stocks:
            stock_data = data.get(stock, {})
            change = stock_data.get('change', 0)
            
            if change > 5:
                signals[stock] = {
                    'signal': 'positive',
                    'weight': 'high',
                    'explanation': 'Explosive move, strong narrative'
                }
            elif change > 2:
                signals[stock] = {
                    'signal': 'positive',
                    'weight': 'high',
                    'explanation': 'Strong momentum, speculative appetite'
                }
            elif change > -2:
                signals[stock] = {
                    'signal': 'neutral',
                    'weight': 'medium',
                    'explanation': 'Volatile but holding, watching'
                }
            elif change > -5:
                signals[stock] = {
                    'signal': 'negative',
                    'weight': 'medium',
                    'explanation': 'Weakness, risk-off pressure'
                }
            else:
                signals[stock] = {
                    'signal': 'negative',
                    'weight': 'high',
                    'explanation': 'Sharp selloff, narrative breaking'
                }
        
        return signals
    
    @staticmethod
    def calculate_all_signals(market_data: Dict) -> Dict:
        """Calculate all model signals"""
        return {
            'macro': ModelLogic.calculate_macro_signals(market_data.get('macro', {})),
            'crypto': ModelLogic.calculate_crypto_signals(
                market_data.get('crypto', {}),
                market_data.get('macro', {})
            ),
            'equities': ModelLogic.calculate_equities_signals(market_data.get('equities', {})),
            'growth': ModelLogic.calculate_growth_signals(market_data.get('growth', {})),
            'highbeta': ModelLogic.calculate_highbeta_signals(market_data.get('highbeta', {}))
        }

