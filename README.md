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

![](https://raw.githubusercontent.com/psychon-night/psychon-night.github.io/refs/heads/main/shared/platform-indicators/platform-linux.svg)

A Discord bot intended for fun and utility\
Built on Python 3.11.6 and 3.12.3

### WARNINGS
- It's recommended to use Python 3.12.3 if possible
- Windows hosts are NOT supported
- Requires systemd

### Requirements
- Linux (only **Ubuntu**, **Debian**, **Arch**, **Mint**, and **Android** have been tested)
- Python 3.10 or newer
- Approximately 1 GB disk space
	- 300-500 MB for source code
	- 500 MB for dependencies
	- Extra space for cache and logs

### Dependencies
- Python 3.10 or newer (`sudo apt install python3.12-full python3.12-dev`)
- Venv (`sudo apt install python3.11-venv`) (optional)
- PyCord (`pip install git+https://github.com/Pycord-Development/pycord.git`)
- DotEnv (`sudo apt install python-dotenv`)
- Nest Asyncio (`pip install nest_asyncio`)
- Asyncio (`pip install asyncio`)
- Python3 systemd  (`sudo apt install python3-systemd`)

For optional QR support, you also need:
- zbar (`sudo apt-get install libzbar0 && pip install pyzbar`)
- Pillow (`pip install pillow`)

**NOTE**: On some systems, it may be neccesary to replace `pip` with `python -m pip` or `python3 -m pip`\
**NOTE**: If you're not using a venv for Fritz, you'll need to add ` --break-system-packages` to the end of each pip command (`pip install py-cord --break-system-packages`, for example)

Obviously, if your system has a package manager like `yay`, use that instead

### Setup
1. Download and extract source code
2. Create your Venv or Anaconda environment (optional, recommended. Do I do this? HAH! NOPE!)
3. Install the [dependencies](#dependencies)
4. At the root of the project, create a file named `.env`
5. Use the [.env template](https://github.com/murderaxolotl/Fritz-for-Discord/blob/main/.env.template) and set your env variables

### Plugins

Fritz supports plugins! These are intended to allow for the modular addition of commands and features. A few default plugins ship by default, but you're welcome to remove them!

Plugins are allowed to hook a few events by including this function:
```
def _funchook() -> tuple[list, list, list]:
	# Signature: [on_ready, on_message, on_error]
	return [], [], []
```

Where each list contains functions to call.\
Fritz will `await` on_message and on_error functions, but NOT on_ready\
Fritz will pass the message context to on_message. Function must take one parameter:  `def my_function(context)`\
Fritz will pass the context and error to on_error. Function must take two parameters: `def my_function(context, error)`

Here's an example:
```
def _funchook() -> tuple[list, list, list]:
	# Signature: [on_ready, on_message, on_error]
	return [print_welcome_message], [scan_message_for_files, scan_message_for_swears], [send_email_to_admin]
```

Where the functions would be defined like this:
```
def print_welcome_message():
	print("Hello, user!")

def scan_message_for_files(context):
	# ...do file scanning here...

def send_email_to_admin(context, error):
	# ...send a nice email here...
```

### Configure
- In `resources/shared.py`, set `INVITE_URL` to your bot's URL, `GIT_URL` to your GitHub URL, and `REGISTERED_DEVELOPERS` to your UUID
- In `resources/shared.py`, set your configuration. Be sure to set these:
	- `DISALLOW_PLATFORM LEAKS`
	- `DISALLOW_SYSINF_LEAKS`
	- `LOGGING_BLACKLIST`

### Command Documentation

To get a list of all commands, use Fritz's `help` slash command
