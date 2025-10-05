import os
import json
import pandas as pd

from requests import get
from steamwebapi.api import ISteamUser, IPlayerService
from time import time

assert os.path.exists("config.json"), f"Fatal error: config.json is missing"

with open("config.json", "r", encoding="UTF-8") as f:
    config = json.loads(f.read())

STEAMSPY_URL = "http://steamspy.com"
STEAM_PROFILE_NAME = config["profile_name"]
STEAM_API_KEY = config["api_key"]
LAST_STATE = "last.json"
DATABASE_FOLDER = "db/"

def get_player_id(profile_name: str, steam_api_key: str) -> int:
    user_info = ISteamUser(steam_api_key=steam_api_key)
    steamid = user_info.resolve_vanity_url(profile_name)['response']['steamid']
    return steamid

def get_owned_games(steam_id: int, steam_api_key: str) -> list:
    player_service = IPlayerService(steam_api_key=steam_api_key)
    games = player_service.get_owned_games(steam_id)['response']['games']
    return games

def get_game_info(game_id: int) -> dict:
    response = get(f'{STEAMSPY_URL}/api.php?request=appdetails&appid={game_id}')
    response.raise_for_status()
    return json.loads(response.text)

def get_playtimes(profile_name, api_key):
    id = get_player_id(profile_name, api_key)
    all_games = get_owned_games(id, api_key)

    return {
        str(game["appid"]): game["playtime_forever"]
        for game in all_games
    }

def get_last_playtimes(fname):
    assert os.path.exists(fname), f"Could not find file {fname}"

    with open(fname, "r", encoding="UTF-8") as f:
        all = json.loads(f.read())
    
    time_of_last_check = all["timestamp"]
    last_playtimes = all["playtimes"]

    return time_of_last_check, last_playtimes

def get_new_games(current_games: set, last_games: set):
    return current_games - last_games

def get_available_games(current_games: set, last_games: set):
    return current_games.intersection(last_games)

def get_updateable_games(avialable_games: set, current_playtimes, last_playtimes):
    ug = []
    for g in avialable_games:
        if current_playtimes[g] > last_playtimes[g]:
            ug.append(g)
    return ug

def save_playtime_state(file_name, current_time, current_playtimes):
    state = {
        "timestamp": current_time,
        "playtimes": current_playtimes
    }

    with open(file_name, "w", encoding="UTF-8") as f:
        f.write(json.dumps(state))

    return None

def append_row(df: pd.DataFrame, row: list) -> pd.DataFrame:
    new_row = pd.DataFrame({
        c : [r] for c, r in zip(df.columns, row)
    })
    return pd.concat([df, new_row], ignore_index=True)

def make_new_game(db_folder: str, appid: int, 
                  time_of_last_check: int,
                  current_time: int, current_playtime: int):
    
    if os.path.exists(db_folder + str(appid) + ".csv"):
        raise Exception(f"Game {appid} already has a file, despite it being claimed as new!")
    df = pd.DataFrame(columns=["time", "total_playtime"])
    df.loc[len(df)] = [time_of_last_check, 0]
    df.loc[len(df)] = [current_time, current_playtime]
    df.to_csv(db_folder + str(appid) + ".csv", index=False)

def update_game(db_folder: str, appid: int,
                time_of_last_check: int,
                current_time: int, current_playtime: int):
    assert time_of_last_check < current_time, f"Current registration time ({current_time}) must be after last check time ({time_of_last_check})."

    if not os.path.exists(db_folder + str(appid) + ".csv"):
        raise Exception(f"Game {appid} does not have a file, despite being claimed as updatable, and hence not new!")

    df = pd.read_csv(db_folder + str(appid) + ".csv")
    last_recording = df.iloc[-1]
    if last_recording.total_playtime == current_playtime:
        raise Exception(f"No need to update, last recorded playtime ({last_recording.total_playtime} is the same as current recorded playtime {current_playtime}).")

    if last_recording.time < time_of_last_check:
        df = append_row(df, [time_of_last_check, last_recording.total_playtime])
        df = append_row(df, [current_time, current_playtime])
    elif last_recording.time == time_of_last_check:
        df = append_row(df, [current_time, current_playtime])
    elif last_recording.time > time_of_last_check:
        raise Exception(f"Time of last recording {last_recording.time} should not be larger than time of last check {time_of_last_check}. Has a check not been recorded?")

    df.to_csv(db_folder + str(appid) + ".csv", index=False)


