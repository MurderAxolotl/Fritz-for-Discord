import discord
import dotenv
import os
import json
import datetime
import systemd.journal as systemd

dotenv.load_dotenv(".env")

# Fritz is always in debug mode on my development system, so I have an env
# var for it. Try to look for said environment variable
# Don't manually edit FORCE_DEBUG, as this might result in unintended
# behaviours
try:
	FRITZ_FORCE_DEBUG:str = os.getenv("fritzDebug")

	if FRITZ_FORCE_DEBUG == "1": FORCE_DEBUG = True
	else: FORCE_DEBUG = False # Environment variable is set, but not 1

except: FORCE_DEBUG = False # Environment variable is not set

if FORCE_DEBUG: IS_DEBUGGING = True
else: IS_DEBUGGING = False # If you want to enable debug mode, change this line

#########################
# CONFIGURATION OPTIONS #
#########################

# True / False; setting to false will limit the
# mcstatus command to the servers listed in 
# ALLOWED_MCSTATUS_SERVERS constant
# The mcstatus command can leak your IP!
LIMIT_MCSTATUS_COMMAND = True

# List of server IDs to allow the mcstatus
# command in
ALLOWED_MCSTATUS_SERVERS = ["1264449432057806920"]

# True / False; set to "True" to disable warnings about what platform Fritz is on. 
# This only hides content Discord-side -- terminal flares will still be shown. 
# THIS DOES NOT DISABLE THE /system OR /info COMMANDS
DISALLOW_PLATFORM_LEAKS = False

# Prevents users not in REGISTERED_DEVELOPERS 
# from using /system and /info commands
DISALLOW_SYSINF_LEAKS = True

# A list of unquoted user IDs to ban from the bot
BLACKLISTED_USERS = list(json.loads(os.getenv("blacklisted_users")))

# The discord invite URL for your bot
INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1070042394009014303&permissions=535260691552&scope=bot"

# The Gitlike URL for your bot
# Please note, this does not have to be Github
# Feel free to use something else, like Gitlab
# I only ask that you provide attribution to me :3
GIT_URL = "https://github.com/psychon-night/Fritz-for-Discord"


###################################
# DON'T EDIT ANYTHING BELOW HERE! #
###################################


# Do our best to determine whether the system is Android-based or not
if os.path.exists("/storage/emulated/0/Android"): IS_ANDROID = True
else:                                             IS_ANDROID = False

# Secrets #
APPLICATIONID = os.getenv("applicationID")
TOKEN         = os.getenv("discordToken")
PLATFORM_IDENTIFIER = "desktop" if not IS_ANDROID else "android"

SPOTIFY_ID = os.getenv("spotifyID")
SPOTIFY_SECRET = os.getenv("spotifySecret")

try: MINECRAFT_SERVER_FIXED_ADDRESS = os.getenv("MINECRAFT_ADDRESS")
except: MINECRAFT_SERVER_FIXED_ADDRESS = ""
try: MINECRAFT_SERVER_PORT = os.getenv("MINECRAFT_PORT")
except: MINECRAFT_SERVER_PORT = ""

# Globals #
QUOTE_WEBHOOK = os.getenv("quote_webhook")
QUOTE_WEBHOOK_FM = os.getenv("quote_webhook_fm")
QUOTE_ID = os.getenv("quotebook_id")
QUOTE_ID_FM = os.getenv("quotebook_id_fm")
REGISTERED_DEVELOPERS = ["1063584978081951814", "1067843602480377907"] # Okay, well, you can probably safely edit this
INTENTS = discord.Intents(messages=True, message_content=True, voice_states=True, reactions=True)

CONTEXTS = {discord.InteractionContextType.bot_dm, discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}
INTEGRATION_TYPES={discord.IntegrationType.guild_install, discord.IntegrationType.user_install}

CONTEXTS_SERVER_ONLY = {discord.InteractionContextType.guild}
INTEGRATION_TYPES_SERVER_ONLY = {discord.IntegrationType.guild_install}

PATH = os.getenv("systemPath")

LOG_SEVERITY = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO"]

class journal:
	""" Interface with systemd logs\n
	Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info` """
	def logDisk(message:str, severity:int=6):
		LOG_LOC = PATH + "/logs/journal"
		

		template = "{date}@{time} - [{sev}] {entry}\n"

		current_time = datetime.datetime.now().strftime("%H:%M:%S")
		today = datetime.date.today()

		if os.path.exists(LOG_LOC):
			with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))
		else:
			with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))

	def log(message:str, severity:int=6):
		""" Write a log message\n
		Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info`
		"""

		journal.logDisk(message, severity)
		systemd.send(message, SYSLOG_IDENTIFIER="fritz", LEVEL=LOG_SEVERITY[severity])

	def log_fatal(message:str):
		""" Logs at the CRITICAL level """
		LOG_LOC = PATH + "/logs/journal"
		template = "{date}@{time} - [CRITICAL] {entry}\n"
		current_time = datetime.datetime.now().strftime("%H:%M:%S")
		today = datetime.date.today()

		if os.path.exists(LOG_LOC):
			with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))
		else:
			with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))

		systemd.send(message, SYSLOG_IDENTIFIER="fritz", LEVEL="critical")

# Why aren't these constants? #
intents = INTENTS
version = f"1.25.2-{PLATFORM_IDENTIFIER}"
