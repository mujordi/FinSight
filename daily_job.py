from macro_model import macro_model
from data_fetcher import get_real_yield,get_dxy,get_vix,get_curve
from storage import save

res=macro_model({'real_yield':get_real_yield(),'dxy':get_dxy(),'vix':get_vix(),'yield_curve':get_curve()})
save(res)
print(res)
