import lib
import json
import pandas as pd
from time import time
from datetime import datetime

with open(lib.EVENT_FILE, "r", encoding="UTF-8") as f:
    events = [
        json.loads(e) 
        for e in list(filter(
            lambda l: len(l) > 0, 
            f.read().split("\n")))]

with open(lib.FIRST_STATE, "r", encoding="UTF-8") as f:
    start_playtimes = json.loads(f.read())

with open(lib.LAST_STATE, "r", encoding="UTF-8") as f:
    last_playtimes = json.loads(f.read())

new_games = []

for e in events:
    for ts, d in e.items():
        for g, pt in d["new"].items():
            new_games.append((g, pt))

updated_games = []

for e in events:
    for ts, d in e.items():
        for g, pt in d["updated"].items():
            updated_games.append((g, pt))

df = pd.DataFrame(columns=last_playtimes.keys())

timestamps = []
for e in events:
    for ts, d in e.items():
        timestamps.append(int(ts))

first_time = min(timestamps)
last_time = max(timestamps)

df.loc[first_time-1, list(start_playtimes.keys())] = list(start_playtimes.values())
df.loc[last_time+1,  list(last_playtimes.keys())] =  list(last_playtimes.values())

for e in events:
    for ts, d in e.items():
        for g, pt in d["new"].items():
            df.loc[ts, g] = pt
        for g, pt in d["updated"].items():
            df.loc[ts, g] = pt

datetime_index = [datetime.fromtimestamp(int(s)) for s in list(df.index)]
df.index = datetime_index
df = df.sort_index()