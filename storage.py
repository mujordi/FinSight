import json
def save(d): json.dump(d, open('state.json','w'), indent=2)