import json
FILE='macro_state.json'

def save(d): json.dump(d,open(FILE,'w'))
def load():
    try: return json.load(open(FILE))
    except: return None
