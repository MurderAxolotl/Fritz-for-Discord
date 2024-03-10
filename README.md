# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

A Discord bot intended for fun and utility

### Dependencies
- Python 3.10 or newer
- PyCord (`pip install py-cord`)
- DotEnv (`pip install python-dotenv`)

### Setup
- Download and extract source code
- Find and remove these lines:
  - `import private.ci_private`
  - `await private.ci_private.ciPrint(message, fs)`
  - `await private.ci_private.autoquote(message)`
- At the root of the project, create a file named `.env`
- Use the [.env template](https://github.com/psychon-night/Fritz-for-Discord/blob/main/.env.template) and set your env variables
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set `AI_BLACKLIST` and `LYRIC_BLACKLIST`

### Stuff you can steal

`scripts/api/discord.py` is pretty nifty, it adds some bindings to the Discord API in a very user-friendly way. Also, it lets you do simple crap (like getting guild info) which PyCord seeems ***INCAPABLE*** of doing correctly. Also it's reasonably self-documenting and understandable (again, looking at you PyCord, your docs are so far out of date it's not even funny)

### Lyric Loader

This stupid little module allows you to drop any text file into `resources/docs/lyrics` and do some fancy stuff. It's best if I explain like so:\
- Place a file named `welcome to the underground` in the lyrics folder (note the lack of a file extension)
- Put some words in it (for example, copy the lyrics for `To the Bone`... Strip the blank spaces though! NO BLANK LINES!)
- Restart the bot [1]
- Go to Discord and type `welcome to the underground`

Pretty cool, yeah?\
Did you see how the trigger words `welcome to the underground` in Discord is the same as the file name? That's how it works! The file name will be the trigger word for this lyric spam

[1] - By default, the bot will take measures to reduce disk IO. This means that lyrics are only cached when the bot starts.\
To change this behaviour, open `shared.py` and set `REDUCE_DISK_READS` to `False`. This will cause the lyrics to be re-cached on EVERY SINGLE MESSAGE EVENT, meaning you get drag-and-drop support :3 (and also a destroyed disk...)

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command
