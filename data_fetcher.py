import requests

def get_fred(series):
    url='https://api.stlouisfed.org/fred/series/observations'
    params={'series_id':series,'file_type':'json','sort_order':'desc','limit':1}
    r=requests.get(url,params=params)
    return float(r.json()['observations'][0]['value'])

def get_real_yield(): return get_fred('DFII10')
def get_curve(): return get_fred('DGS10')-get_fred('DGS2')
def get_yahoo(s): return requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={s}').json()['quoteResponse']['result'][0]['regularMarketPrice']
def get_dxy(): return get_yahoo('DX-Y.NYB')
def get_vix(): return get_yahoo('^VIX')
