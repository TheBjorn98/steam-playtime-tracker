import lib
import json
import os

pid = lib.get_player_id(lib.STEAM_PROFILE_NAME, lib.STEAM_API_KEY)
all_games = lib.get_owned_games(pid, lib.STEAM_API_KEY)

current_playtimes = {
    str(game["appid"]): game["playtime_forever"]
    for game in all_games
}

assert not os.path.exists(lib.FIRST_STATE), f"{lib.FIRST_STATE} already exists, manually remove to overwrite"
assert not os.path.exists(lib.LAST_STATE), f"{lib.LAST_STATE} already exists, manually remove to overwrite"
assert not os.path.exists(lib.EVENT_FILE), f"{lib.EVENT_FILE} already exists, manually remove to overwrite"

with open(lib.FIRST_STATE, "w", encoding="UTF-8") as f:
    f.write(json.dumps(current_playtimes))

with open(lib.LAST_STATE, "w", encoding="UTF-8") as f:
    f.write(json.dumps(current_playtimes))

with open(lib.EVENT_FILE, "w", encoding="UTF-8") as f:
    pass