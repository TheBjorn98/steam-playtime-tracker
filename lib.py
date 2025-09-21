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
FIRST_STATE = "first.json"
LAST_STATE = "last.json"
EVENT_FILE = "events.json"

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

def get_new_games(last_playtimes, current_playtimes):
    ng = list(set(current_playtimes) - set(last_playtimes))
    return {g: current_playtimes[g] for g in ng}

def get_updated_games(last_playtimes, current_playtimes):
    ug =  list(filter(
        lambda k: last_playtimes[k] != current_playtimes[k], 
        last_playtimes.keys()))
    return {g: current_playtimes[g] for g in ug}

def get_playtimes(profile_name, api_key):
    id = get_player_id(profile_name, api_key)
    all_games = get_owned_games(id, api_key)

    return {
        str(game["appid"]): game["playtime_forever"]
        for game in all_games
    }
