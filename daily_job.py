
from datetime import datetime
from data_fetcher import snapshot, series
from macro_core import macro_core
from asset_layer import assets
from products import PRODUCT_TABS
from storage import save

macro=macro_core(snapshot())
state={
 "updated":datetime.utcnow().isoformat(),
 "macro":macro,
 "assets":assets(macro["state"]),
 "tabs":PRODUCT_TABS,
 "series":series()
}
save(state)
print(state)
