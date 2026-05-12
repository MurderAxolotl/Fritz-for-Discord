##############################################################
##############################################################
#### CONFIGURATION IS NO LONGER IN THIS FILE! DO NOT EDIT ####
####  INSTEAD, EDIT YOUR ENV FILE! CHECK THE TEMPLATE ON  ####
####              GITHUB FOR THE NEW TEMPLATE             ####
##############################################################
##############################################################

import discord
import dotenv
import os
import sys
import json
import string
import random

dotenv.load_dotenv(".env")

LOG_SEVERITY = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG"]

# Fritz is always in debug mode on my development system, so I have an env
# var for it. Try to look for said environment variable
# Don't manually edit FORCE_DEBUG, as this might result in unintended
# behaviours
try:
	FRITZ_FORCE_DEBUG:str = os.getenv("fritzDebug", "0")

	if FRITZ_FORCE_DEBUG == "1":
		FORCE_DEBUG = True
	else:
		FORCE_DEBUG = False # Environment variable is set, but not 1

except Exception:
	FORCE_DEBUG = False # Environment variable is not set

if FORCE_DEBUG: IS_DEBUGGING = True
else: IS_DEBUGGING = False # If you want to enable debug mode, change this line

LOG_LEVEL_STRING:str = os.getenv("log_level", "INFO")

if LOG_LEVEL_STRING.isnumeric():
	LOG_LEVEL:int = int(LOG_LEVEL_STRING)
else:
	LOG_LEVEL:int = LOG_SEVERITY.index(LOG_LEVEL_STRING)

ENABLE_IMPORTED_PLUGINS = str(os.getenv("enable_plugins", "False")) == "True"

LIMIT_MCSTATUS_COMMAND = str(os.getenv("limit_mcs_command", "False")) == "True"
DISALLOW_PLATFORM_LEAKS = str(os.getenv("hide_platform", "False")) == "True"
DISALLOW_SYSINF_LEAKS = str(os.getenv("block_sysinf_leaks", "False")) == "True"

# The discord invite URL for your bot
INVITE_URL = os.getenv("invite_url", "")

# The Gitlike URL for your bot
# Please note, this does not have to be Github
# Feel free to use something else, like Gitlab
# I only ask that you provide attribution to me :3
GIT_URL = os.getenv("git_url", "")

# The path to PtK's extracted AND FORMATTED resources
PTK_FOLDER = os.getenv("ptkPath", "")

###################################
# DON'T EDIT ANYTHING BELOW HERE! #
###################################

# Do our best to determine whether the system is Android-based or not
if os.path.exists("/storage/emulated/0/Android"): IS_ANDROID = True
else:                                             IS_ANDROID = False

# Secrets #
APPLICATIONID = os.getenv("applicationID", "")
TOKEN         = os.getenv("discordToken", "")
PLATFORM_IDENTIFIER = "desktop" if not IS_ANDROID else "android"

try:
	MINECRAFT_SERVER_FIXED_ADDRESS = os.getenv("MINECRAFT_ADDRESS", "")
except:
	MINECRAFT_SERVER_FIXED_ADDRESS = ""

try:
	MINECRAFT_SERVER_PORT = os.getenv("MINECRAFT_PORT", "")
except:
	MINECRAFT_SERVER_PORT = ""

ALLOWED_MCSTATUS_SERVERS = json.loads(os.getenv("mcs_whitelist", "[]"))
BLACKLISTED_USERS = list(json.loads(os.getenv("blacklisted_users", "{}")))

# Globals #
REGISTERED_DEVELOPERS = json.loads(os.getenv("developers", "[]")) # Okay, well, you can probably safely edit this
INTENTS = discord.Intents(messages=True, message_content=True, voice_states=True, reactions=True)

CONTEXTS = {discord.InteractionContextType.bot_dm, discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}
INTEGRATION_TYPES={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}

CONTEXTS_SERVER_ONLY = {discord.InteractionContextType.guild}
INTEGRATION_TYPES_SERVER_ONLY = {discord.IntegrationType.guild_install}

PATH = os.getenv("systemPath", sys.path[0])
CONFIG_PATH = os.getenv("configPath", PATH + "/config")
RESOURCE_PATH = os.getenv("resourcePath", PATH + "/resources")
PLUGIN_PATH = os.getenv("pluginPath", PATH + "/plugins")
CACHE_PATH = os.getenv("cachePath", PATH + "/cache")

VERSION = f"1.27.1-{PLATFORM_IDENTIFIER}"
BOOTID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
