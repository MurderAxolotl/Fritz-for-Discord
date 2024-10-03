import discord, dotenv, os, json, sys
from types import NoneType

dotenv.load_dotenv(".env")

IS_DEBUGGING = False

# Do our best to determine whether the system is Android-based or not
if os.path.exists("/storage/emulated/0/Android"): IS_ANDROID = True
else:                                             IS_ANDROID = False

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1070042394009014303&permissions=535260691552&scope=bot"
GIT_URL = "https://github.com/psychon-night/Fritz-for-Discord"

# Secrets #
APPLICATIONID = os.getenv("applicationID")
TOKEN         = os.getenv("discordToken")
CT_NAMES      = json.loads(os.getenv("ct_name_map"))
TEST_NAMES    = json.loads(os.getenv("test_name_map"))
PLATFORM_IDENTIFIER = "desktop" if not IS_ANDROID else "android"

# Globals #
QUOTE_WEBHOOK = os.getenv("quote_webhook")
REGISTERED_DEVELOPERS = ["1063584978081951814", "1067843602480377907"]
INTENTS = discord.Intents(messages=True, message_content=True, voice_states=True)

CONTEXTS = {discord.InteractionContextType.bot_dm, discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}
INTEGRATION_TYPES={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}

CONTEXTS_SERVER_ONLY = {discord.InteractionContextType.guild}
INTEGRATION_TYPES_SERVER_ONLY = {discord.IntegrationType.guild_install}

PATH = os.getenv("systemPath")

# Configuration Parameters
DISALLOW_PLATFORM_LEAKS = False # True / False; set to "True" to disable warnings about what platform Fritz is on. This only hides content Discord-side -- terminal flares will still be shown. THIS DOES NOT DISABLE THE /system OR /info COMMANDS
DISALLOW_SYSINF_LEAKS = True # Prevents users not in REGISTERED_DEVELOPERS from using /system and /info commands
ENABLE_LOGGING    = True # True / False; whether to log messages sent to channels Fritz has read access to
LOGGING_BLACKLIST = [] # A list of NON-QUOTED server IDs to block logging

BLACKLISTED_USERS = list(json.loads(os.getenv("blacklisted_users"))) # A list of NON-QUOTED user IDs to ban from using the bot

# Why aren't these constants? #
intents = INTENTS
version = f"1.21.1-{PLATFORM_IDENTIFIER}"

# Mappings because I can't be bothered to fix stuff #
registeredDevelopers = REGISTERED_DEVELOPERS
