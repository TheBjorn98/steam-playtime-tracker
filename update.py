import lib
import time

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