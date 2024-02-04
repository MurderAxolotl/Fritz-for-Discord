# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

A Discord bot intended for fun and utility

Requires Python 3.10+

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
> `pp_users query_string`: Query Pronouns Page for a user\
> `pp_terms query_string`: Query Pronouns Page for a term

> `seasify song_title count`: Search Spotify for a song\
*count*: int between 1 and 25

> `chatgpt prompt legacy_mode`: Interact with ChatGPT\
*legacy_mode*: allows you to use a legacy LLM. See built-in autocomplete for options

> `cai message character reset`: Interact with a Character AI character\
*character*: defines what character totalk to. See built-in autocomplete for options\
*reset*: whether to continue the current conversation (keep memory) or reset it

> `qr create data style`: Create a QR code\
*data*: the data to encode into the QR code\
*style*: which QR style to use. Default is stylised. Set to `compatible` to make a generic QR code

> `qr scan url`: Scan a QR code.  Must be publically available on the internet (such as on imgur)\
*url*: link to an image containing the QR code

> `givecat`: Get a random cat image

> `joke`: Get a random joke from the internet

> `check_nsfw_allowed`

> `ping`: Check the bot's ping in milliseconds

> `about`: Get the bot's current version

> `invite`: Get the bot's invite URL
