# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

A Discord bot intended for fun and utility\
Built on Python 3.11.6

### WARNINGS
- Currently uses a beta version of PyCord!
	- Install PyCord, then run `pip install git+https://github.com/Pycord-Development/pycord@feat/ua`

### Dependencies
- Python 3.10 or newer (`sudo apt install python3.11-full python3.11-dev`)
- Venv (`sudo apt install python3.11-venv`)
- PyCord (`pip install py-cord`)
- DotEnv (`sudo apt install python-dotenv`)
- g4f (`pip install g4f`)
- zbar (`pip install pyzbar`)
- CAI (`pip install characterai`)
- Nest Asyncio (`pip install nest_asyncio`)
- Asyncio (`pip install asyncio`)
- Pillow (`pip install pillow`)
- BS4 (`pip install bs4`)

### Setup
- Download and extract source code
- Install dependencies: `pip install py-cord python-dotenv g4f pyzbar characterai asyncio nest_asyncio pillow bs4`
- Create a folder named `cache`
- At the root of the project, create a file named `.env`
- Use the [.env template](https://github.com/psychon-night/Fritz-for-Discord/blob/main/.env.template) and set your env variables

### Configure
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set `AI_BLACKLIST` and `LYRIC_BLACKLIST`

### Portable Modules

These are .py files you can use in your own projects. Please give credit!

`scripts/api/discord.py`: an up-to-date and easy to use API wrapper for extremely common use-cases. Designed to fill the gaps of PyCord; it is NOT a replacement for PyCord

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command
