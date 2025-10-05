import argparse
import lib
import sys
import os
import time

def _initialize():
    if not os.path.exists(lib.LAST_STATE):
        lib.save_playtime_state(lib.LAST_STATE, int(time.time()), {})

def _update():
    cp = lib.get_playtimes(lib.STEAM_PROFILE_NAME, lib.STEAM_API_KEY)
    last_check_time, lp = lib.get_last_playtimes(lib.LAST_STATE)
    current_check_time = int(time.time())

    cg = set(cp)
    lg = set(lp)

    ng = lib.get_new_games(cg, lg)
    avg = lib.get_available_games(cg, lg)
    ug = lib.get_updateable_games(avg, cp, lp)

    for g in ng:
        lib.make_new_game(lib.DATABASE_FOLDER, g, 
                        last_check_time, current_check_time, cp[g])

    for g in ug:
        lib.update_game(lib.DATABASE_FOLDER, g, 
                        last_check_time, current_check_time, cp[g])

    lib.save_playtime_state(lib.LAST_STATE, current_check_time, cp)

if __name__ == "__main__":
    args = sys.argv[1:]

    if args[0] == "init":
        _initialize()
    elif args[0] == "update":
        _update()
    else:
        pass