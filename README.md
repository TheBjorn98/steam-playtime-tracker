# steam-playtime-tracker
The code is not very good at the moment, but there's almost a proof-of-concept.
The idea is that this can be run as a daemon and collect data about your playtime.
Right now, everything is a hot mess, because I am scared of databases and have in general no idea what's happening.

## Config

One must create a `config.json` file with the following structure:

```json
{
    "profile_name": "your steam profile name",
    "api_key": "your steam api key"
}
```

#todo: Write some words on how to get the api key and everything

## Notes

- This is still very much a "work in progress"
- I am slightly abusing the json specification (`events.json` is not compliant), but that's fine, no worries
- I'll probably refactor to use the built-in `cmd` package, but who knows when
- `requirements.txt`? Never heard of, but we're using `pandas, numpy, requests, steamwebapi` and some other things


Good luck, have fun.