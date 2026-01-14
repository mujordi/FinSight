
import datetime, json
from data_fetcher import snapshot, series
from macro_core import macro_core

state={
 "date":datetime.date.today().isoformat(),
 "macro":macro_core(snapshot()),
 "series":series()
}
json.dump(state,open("state.json","w"),indent=2)
print(state)
