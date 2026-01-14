
from macro_model import macro_model
from gold_model import gold_model
from nasdaq_model import nasdaq_model
from data_fetcher import get_real_yield, get_dxy, get_vix, get_curve
from storage import save

macro = macro_model({
    "real_yield": get_real_yield(),
    "dxy": get_dxy(),
    "vix": get_vix(),
    "yield_curve": get_curve()
})

data = {
    "macro": macro,
    "gold": gold_model(macro),
    "nasdaq": nasdaq_model(macro)
}

save(data)
print(data)
