# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

A Discord bot intended for fun and utility

### Dependencies
- Python 3.10 or newer
- PyCord (`pip install py-cord`)
- DotEnv (`pip install python-dotenv`)

### Setup
- Download and extract source code
- Open `main.py`, then find and remove these lines:
  - `import private.ci_private`
  - `await private.ci_private.ciPrint(message, fs)`
  - `await private.ci_private.autoquote(message)`
- At the root of the project, create a file named `.env`
- Use the [.env template](https://github.com/psychon-night/Fritz-for-Discord/blob/main/.env.template) and set your env variables
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set `AI_BLACKLIST` and `LYRIC_BLACKLIST`

### Portable Modules

These are .py files you can use in your own projects. Please give credit!

`scripts/api/discord.py`: an up-to-date and easy to use API wrapper for extremely common use-cases. Designed to fill the gaps of PyCord; it is NOT a replacement for PyCord

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command
