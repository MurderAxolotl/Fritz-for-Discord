# Fritz

== We're Using GitHub Under Protest ==

This project is currently hosted on GitHub.  This is not ideal; GitHub is a
proprietary, trade-secret system that is not Free and Open Souce Software
(FOSS).  We are deeply concerned about using a proprietary system like GitHub
to develop our FOSS project.  We urge you to read about the
[Give up GitHub](https://GiveUpGitHub.org) campaign from
[the Software Freedom Conservancy](https://sfconservancy.org) to understand
some of the reasons why GitHub is not a good place to host FOSS projects.

Any use of this project's code by GitHub Copilot, past or present, is done
without our permission.  We do not consent to GitHub's use of this project's
code in Copilot.

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](https://forthebadge.com) 

![](https://raw.githubusercontent.com/psychon-night/psychon-night.github.io/refs/heads/main/shared/platform-indicators/platform-linux.svg) ![](https://raw.githubusercontent.com/psychon-night/psychon-night.github.io/refs/heads/main/shared/platform-indicators/platform-android.svg)

A Discord bot intended for fun and utility\
Built on Python 3.11.6, unfortunately tested on 3.12

### WARNINGS
- Some commands do not respect the ENABLE_LOGGING setting
	- Please note: I added this long before Fritz was this fragmented. Mostly unimportant now
- It's recommended to use Python 3.12.3 if possible
- Intended for use on **Linux**
	- Android (through Termux) is supported (on versions before 1.24)

### Requirements
- Linux (only **Ubuntu**, **Debian**, **Arch**, **Mint**, and **Android** have been tested)
- Python 3.10 or newer
- Approximately 1 GB disk space
	- 300-500 MB for source code
	- 500 MB for dependencies
	- Extra space for cache and logs
- Currently uses an unmerged version of PyCord for Starboard features
	- pip install git+https://github.com/NeloBlivion/pycord.git@forwarding
		- Thank you NeloBlivion for this awesome feature <3

### Dependencies
- Python 3.10 or newer (`sudo apt install python3.11-full python3.11-dev`)
- Venv (`sudo apt install python3.11-venv`)
- PyCord (`pip install py-cord`)
- DotEnv (`sudo apt install python-dotenv`)
- zbar (`sudo apt-get install libzbar0 && pip install pyzbar`)
- Nest Asyncio (`pip install nest_asyncio`)
- Asyncio (`pip install asyncio`)
- Pillow (`pip install pillow`)
- BS4 (`pip install bs4`)
- Python3 systemd  (`sudo apt install python3-systemd`)

**NOTE**: On some systems, it may be neccesary to replace `pip` with `python -m pip` or `python3 -m pip`
**NOTE**: If you're not using a venv for Fritz, you'll need to add ` --break-system-packages` to the end of each pip command (`pip install py-cord --break-system-packages`, for example)

Obviously, if your system has a package manager like `yay`, use that instead

### Setup
1. Download and extract source code
2. Create your Venv or Anaconda environment (optional, recommended. Do I do this? HAH! NOPE!)
3. Install [dependencies](#dependencies)
4. Create a folder named `cache`
5. At the root of the project, create a file named `.env`
6. Use the [.env template](https://github.com/psychon-night/Fritz-for-Discord/blob/main/.env.template) and set your env variables

### Configure
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, `GIT_URL` to your GitHub URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set your configuration. Be sure to set these:
	- `DISALLOW_PLATFORM LEAKS`
	- `DISALLOW_SYSINF_LEAKS`
	- `ENABLE_LOGGING`
	- `LOGGING_BLACKLIST`

### Portable Modules

These are .py files you can use in your own projects. Please give credit!

`scripts/api/discord.py`: an up-to-date and easy to use API wrapper for common use-cases. Designed to fill the gaps of PyCord; it is NOT a replacement for PyCord

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command