# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com) 

A Discord bot intended for fun and utility\
Built on Python 3.11.6

### WARNINGS
- Currently uses a beta version of PyCord!
- Some commands do not respect the ENABLE_LOGGING setting
- Versions of Python other than 3.11.6 are **untested**
- Intended for use on **Linux**. Windows and MacOS are **untested**

### Requirements
- Linux (only **Ubuntu** and **Debian** have been tested)
- Python 3.10 or newer
- Approximately 1 GB disk space
	- 300-500 MB for source code
	- 500 MB for dependencies
	- Extra space for cache and logs

### Dependencies
- Python 3.10 or newer (`sudo apt install python3.11-full python3.11-dev`)
- Venv (`sudo apt install python3.11-venv`)
- PyCord
	1. Install PyCord: `pip install py-cord`
	2. Install the UA features: `pip install git+https://github.com/Pycord-Development/pycord@feat/ua`
- DotEnv (`sudo apt install python-dotenv`)
- g4f (`pip install g4f`)
- zbar (`pip install pyzbar`)
- KramCat's CharacterAI (`pip install git+https://github.com/kramcat/CharacterAI.git`)
- Nest Asyncio (`pip install nest_asyncio`)
- Asyncio (`pip install asyncio`)
- Pillow (`pip install pillow`)
- BS4 (`pip install bs4`)

Obviously, if your system has a package manager like `yay`, use that instead

### Setup
1. Download and extract source code
2. Create your Venv or Anaconda environment
3. Install [dependencies](#dependencies)
4. Create a folder named `cache`
5. At the root of the project, create a file named `.env`
6. Use the [.env template](https://github.com/psychon-night/Fritz-for-Discord/blob/main/.env.template) and set your env variables

### Configure
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, `GIT_URL` to your GitHub URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set `AI_BLACKLIST` and `LYRIC_BLACKLIST`
- In `resources/shared.py`, set `ENABLE_LOGGING`, `LOGGING_BLACKLIST`, and `BLACKLISTED_USERS`

### Portable Modules

These are .py files you can use in your own projects. Please give credit!

`scripts/api/discord.py`: an up-to-date and easy to use API wrapper for extremely common use-cases. Designed to fill the gaps of PyCord; it is NOT a replacement for PyCord

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command
