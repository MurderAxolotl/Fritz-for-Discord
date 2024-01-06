import discord, dotenv, os, json

from types import NoneType

dotenv.load_dotenv(".env")

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1070042394009014303&permissions=535260691552&scope=bot"

# Secrets #
TOKEN = os.getenv("discordToken")
CHATGPT_TOKEN = os.getenv("chatgptToken")
CAI_TOKEN = os.getenv("charAIToken")
CT_NAMES = json.loads(os.getenv("ct_name_map"))
TEST_NAMES = json.loads(os.getenv("test_name_map"))

# Globals #
REGISTERED_DEVELOPERS = ["1063584978081951814", "1067843602480377907"]

# Configuration Parameters
ENABLE_LOGGING    = True # True / False; whether to log messages sent to channels Fritz has read access to
LOGGING_BLACKLIST = [] # A list of NON-QUOTED server IDs to block logging

AI_BLACKLIST = [1192958435608760321] # A list of NON-QUOTED server IDs to block logging

# Why aren't these constants? #
intents = discord.Intents(messages=True, message_content=True, voice_states=True)
version = "1.14.1"

# Mappings because I can't be bothered to fix stuff #
registeredDevelopers = REGISTERED_DEVELOPERS