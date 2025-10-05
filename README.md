# steam-playtime-tracker
The code is not very good at the moment, but there's almost a proof-of-concept.
The idea is that this can be run as a daemon and collect data about your playtime.
Code could be better, but I am scared of databases.

The main feature of the program is to query Steam for the current "forever_playtimes"
for each appid and save it to individual csv-files.
The saving logic takes into account whether a game/appid has updated and skips saving anything if there is no change.
Hence, only games that have been updated since the last query will be recorded.

The program can be run periodically by setting up some recurring way of running
`python track-steam-playtime.py update`.

## Config

One must create a `config.json` file with the following structure:

```json
{
    "profile_name": "your steam profile name",
    "api_key": "your steam api key"
}
```

### How to get a Steam API key

#todo: Write some words on how to get the api key and everything

## Usage

`track-steam-playtime.py` is able to run two commands:

- `init` which initializes the `last.json` file
- `update` which gets info about current playtimes from Steam and creates/appends to appids if necessary

The initialization `init` must be run before one can run `update`.
In order to run the program, a `config.json` file must be present.


### Issues

- If a game gets identified as new, but there is already a file associated with the appid, the program will raise an exception.
    - This can be "fixed" by deleting the file in question, `make_new_game` will create a new file for it.
    - Already recorded data will be lost, but in principle, an already-recorded game should not be wrongly identified as new.
- If a game gets identified as "updatable", but there is no file associated with the appid, the program will also raise an exception.
    - This should also not happen in principle.
    - If it happens, it means that `last.json` contains the playtime for that appid, but for some reason it was never saved to disk.

## Notes

- This is still very much a "work in progress"
- `requirements.txt`? Never heard of, but we're using `pandas, numpy, requests, steamwebapi` and some other things

Good luck, have fun.