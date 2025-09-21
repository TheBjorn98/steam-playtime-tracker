import json
import pandas as pd
import lib

from requests import get
from steamwebapi.api import ISteamUser, IPlayerService
from time import time

id = lib.get_player_id(lib.STEAM_PROFILE_NAME, lib.STEAM_API_KEY)
all_games = lib.get_owned_games(id, lib.STEAM_API_KEY)

# Read the last playtimes for the steam user
with open(lib.LAST_STATE, "r", encoding="UTF-8") as f:
    last_playtimes = json.loads(f.read())

# Get current playtimes from the server
current_playtimes = {
    str(game["appid"]): game["playtime_forever"]
    for game in all_games
}

# Find the new games and the updated games among these sets
new_games = list(
    set(current_playtimes) - set(last_playtimes))
updated_games = list(
    filter(
        lambda k: last_playtimes[k] != current_playtimes[k], 
        last_playtimes.keys()))

# Record both the new and updated games
event_dict = {
    str(int(time())): {
        "new": lib.get_new_games(last_playtimes, current_playtimes),
        "updated": lib.get_updated_games(last_playtimes, current_playtimes)
    }
}

# Append event to the event-file
with open(lib.EVENT_FILE, "a", encoding="UTF-8") as f:
    f.write(json.dumps(event_dict))
    f.write("\n")

# Write the up-to-date "last playtimes"
with open(lib.LAST_STATE, "w", encoding="UTF-8") as f:
    f.write(json.dumps(current_playtimes))