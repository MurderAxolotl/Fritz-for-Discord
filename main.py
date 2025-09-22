"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import scripts.hooks.firstRun
import scripts.hooks.createConfigs # NOQA

import os
import asyncio
import nest_asyncio
import discord
import time
import sys

from resources.shared import CONTEXTS, CONTEXTS_SERVER_ONLY, INTEGRATION_TYPES, INTEGRATION_TYPES_SERVER_ONLY
from resources.shared import BLACKLISTED_USERS, DISALLOW_SYSINF_LEAKS, DISALLOW_PLATFORM_LEAKS, GIT_URL, IS_ANDROID
from resources.shared import IS_DEBUGGING, VERSION, TOKEN, REGISTERED_DEVELOPERS, INVITE_URL
from resources.shared import ENABLE_QUOTEBOOK, ENABLE_IMPORTED_PLUGINS, PATH, BOOTID
from resources.responses import help_messages

from resources.colour import RED, DRIVES, YELLOW, SPECIALDRIVE, BLUE, RESET, MAGENTA, SEAFOAM

import scripts.api.ptk_reactions      as ptk_reactions
import scripts.api.qrTools            as qrTools
import scripts.api.fun                as oneOff
import scripts.api.animal_images      as animals
import scripts.api.discord            as discord_fancy
import scripts.api.lumos_status       as lumos_status
import scripts.api.starboard          as starboard
import scripts.errors.commandCheck    as commandCheck

import scripts.tools.journal          as journal

from scripts.tools.utility import isDeveloper, bannedUser, loadString

# Before anything else, log the boot ID #
journal.___lognoprefix(f"=========== BOOT {BOOTID} ===========", 6)

num_imported_plugins  = 0
errors_during_startup = 0
module_failures = []
general_errors  = []

bot = discord.Bot()
loop = asyncio.get_event_loop()

# Some minor fixes for asyncio
nest_asyncio.apply(loop)

### COMMAND GROUPS ###
fritz = bot.create_group("f",          "Fritz's generic commands",           contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)
zdev  = bot.create_group("f_dev",      "Developer-only utilities",           contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)

if not qrTools.NOQR:
	qr    = bot.create_group("qr",         "Tools relating to QR codes",         contexts=CONTEXTS,         integration_types=INTEGRATION_TYPES)

### SERVER-ONLY COMMANDS ###
sonly = bot.create_group("fs",         "Fritz's server-only commands",   contexts=CONTEXTS_SERVER_ONLY, integration_types=INTEGRATION_TYPES_SERVER_ONLY)

### GLOBAL CHECKS ###
@bot.check
async def global_isbanned_check(ctx):
	if ctx.author.id in BLACKLISTED_USERS:
		journal.log(f"Denying use to banned user {ctx.author.id} ({ctx.author.name})")
		raise bannedUser("You are banned from using Fritz")

	return True

### ===================================== ###
### EVENTS ###
_on_message_hooks = []
_on_ready_hooks = []
_on_application_command_error_hooks = []

# Listen for reactions. Used for starboard features
if not starboard.NOQB:
	@bot.event
	async def on_raw_reaction_add(reactionContext:discord.RawReactionActionEvent):
		await starboard.reactionAdded(reactionContext, bot)

# Listen for "All stay strong"
@bot.event
async def on_message(message):
	if str(message.content).lower() == "all stay strong":
		await message.channel.send("We live eternally")

	for func in _on_message_hooks:
		await func(message)

#  Listen for command errors
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
	await commandCheck.on_command_error(ctx, error)

	for func in _on_application_command_error_hooks:
		await func(ctx, error)

# Wait for the bot to be ready
@bot.event
async def on_ready():
	global errors_during_startup

	startup_text = MAGENTA + "Connected"

	journal.log("Fritz is connected to Discord")

	if errors_during_startup != 0:
		journal.log(f"Encountered {errors_during_startup} errors during startup", severity=5)

		startup_text = startup_text + f" with {RED}{errors_during_startup} errors{RESET}"

		if len(BLACKLISTED_USERS) != 0:
			startup_text = startup_text + f"{MAGENTA}, {YELLOW}{len(BLACKLISTED_USERS)} blacklisted users"

	elif len(BLACKLISTED_USERS) != 0:
		startup_text = startup_text + f" with {YELLOW}{len(BLACKLISTED_USERS)} blacklisted users"

	if num_imported_plugins != 0:
		if errors_during_startup != 0 or len(BLACKLISTED_USERS) > 0:
			startup_text = startup_text + f", {SEAFOAM}{num_imported_plugins} plugins{RESET}"

		else:
			startup_text = startup_text + f" with {SEAFOAM}{num_imported_plugins} plugins{RESET}"

	print(startup_text)

	if len(module_failures) > 0:
		for failure in module_failures:
			journal.log_and_print(f"   => Module '{failure}' failed to import", severity=5)

	if len(general_errors) > 0:
		for failure in general_errors:
			journal.log_and_print(f"   => {failure}", severity=5)

	for func in _on_ready_hooks:
		func()

### ===================================== ###
### RIGHT-CLICK COMMANDS ###
if ENABLE_QUOTEBOOK:
	@bot.message_command(name="Quotebook", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def quotebookContext(ctx:discord.ApplicationCommand, message:discord.Message):
		authorName = message.author.display_name
		author     = message.author.id
		text       = message.content
		avat       = message.author.display_avatar.url

		await oneOff.quotebookMessage(ctx, text, author, authorName, avat)

	# @bot.message_command(name="Quotebook (via Forward)", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	# async def forwardToQuotebook(ctx, message:discord.Message):
	# 	await oneOff.forwardToQuotebook(ctx, message, bot)

### ===================================== ###
### API COMMANDS ###

# CHECK IF THE CONFIGURED MINECRAFT SERVER IS ONLINE #
if not lumos_status.NOMCS:
	@fritz.command(name="mcstatus", description="Check if the Minecraft server is online")
	async def mcstatus(ctx, sendplayerlist:bool=False): await lumos_status.getServerStatus(ctx, sendplayerlist)

### ===================================== ###
### QR CODES ###

# SCAN A QR CODE #
if not qrTools.NOQR:
	@qr.command(name="scan", description="Scan a QR code", pass_context=True)
	async def scanQR(ctx, qr_code_image: discord.Attachment):
		await qrTools.read_cv(ctx, qr_code_image.url)

	# CREATE A QR CODE #
	@qr.command(name="create", description="Make a QR code", pass_context=True)
	async def makeQR(ctx, qr_data, style_mode:discord.Option(str, choices=qrTools.designTypes, description='QR style')="stylized (default)"): #type:ignore
		await qrTools.createQR(ctx, qr_data, style_mode)

else:
	errors_during_startup += 1
	module_failures.append("QR Tools")

### ===================================== ###
### Reaction images from Promises to Keep. These are NOT shipped with Fritz ###
### BECOME FURRIFIED (yeah i'm a furry if you didn't realize that) ###

if not ptk_reactions.NOPTK:
	try:
		@fritz.command(name="artemis_reaction", description="The funny bird man")
		async def artemisReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.ARTEMIS)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "artemis", sprite)

		@fritz.command(name="rofi_reaction", description="Depressed disappointment of a dog")
		async def rofiReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.ROFI)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "rofi", sprite)

		@fritz.command(name="theo_reaction", description="Father figure we all need")
		async def theoReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.THEO)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "theo", sprite)

		@fritz.command(name="gremlin_reaction", description="Little shit is adorable")
		async def gremlinReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.GREMLIN)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "gremlin", sprite)

		@fritz.command(name="hunter_reaction", description="Daddy? Sorry. Daddy? Sorry. Daddy? Sorry-")
		async def hunterReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.HUNTER)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "hunter", sprite)

		@fritz.command(name="friend_reaction", description="Why so angy tho")
		async def friendReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.FRIEND)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "friend", sprite)

		@fritz.command(name="ollie_reaction", description="AUTISTIC")
		async def ollieReaction(ctx, sprite:discord.Option(str, choices=ptk_reactions.OLLIE)): #type:ignore
			await ptk_reactions.reaction_image(ctx, "ollie", sprite)

	except Exception as err:
		journal.log("PtK reactions unavailable: " + str(err), 4)
		errors_during_startup += 1

		module_failures.append("PTK Reactions")

### ===================================== ###
### ANIMAL CONTENT ###

# PICTURES #
# CAT PICTURE #
@fritz.command(name="givecat", description="Get a random cat photo")
async def givecat(ctx): await animals.giveCat(ctx)

# LYNX PICTURE #
@fritz.command(name="givelynx", description="Get a random lynx photo")
async def givelynx(ctx): await animals.giveLynx(ctx)

# FOX PICTURE #
@fritz.command(name="givefox", description="Get a random fox photo")
async def givefox(ctx): await animals.giveFox(ctx)

# RACOON PICTURE #
@fritz.command(name="giveracc", description="Get a random raccoon photo (or video)")
async def trashpanda(ctx, video:bool=False): await animals.giveTrashPanda(ctx, video)

# WAH IMAGE #
@fritz.command(name="givewah", description="Get a random red panda photo")
async def wahimage(ctx): await animals.giveWah(ctx)

# FACTS #
# RACOON FACTS #
@fritz.command(name="raccfacc", description="Get a random raccoon fact")
async def raccfacc(ctx): await animals.giveRaccFacc(ctx)

# WAH FACT #
@fritz.command(name="wahfact", description="Get a random red panda fact")
async def wahfact(ctx): await animals.giveWahFact(ctx)

### ===================================== ###
### SERVER-ONLY COMMANDS ###

### ===================================== ###
### USER MANAGEMENT ###

### ===================================== ###
### BOT UTILITIES ###
@fritz.command(name='bug', description='Report a bug')
async def bugreport(ctx):
	await ctx.respond(loadString("/bug_report").format(GITHUB_BASE=GIT_URL), ephemeral=True)

@fritz.command(name='ping', description='Get Fritz\'s current ping')
async def ping(ctx):
	latency = round(bot.latency * 1000)
	await ctx.respond('Current latency: ' + str(latency) + "ms")

### ===================================== ###
### INFORMATION COMMANDS ###
@fritz.command(name="help", description="Stop and RTFM", pass_context=True)
async def help(ctx):
	await ctx.respond(loadString("/commands"), ephemeral=True)

@fritz.command(name="changelog", description="See past changes to Fritz", pass_context=True)
async def changelog(ctx):
	await ctx.respond(file=help_messages.changelog, ephemeral=True)

## Get info about Fritz ##
@fritz.command(name="system", description="Advanced system info", pass_context=True)
async def sysinfo(ctx):
	if DISALLOW_SYSINF_LEAKS and not (str(ctx.author.id) in REGISTERED_DEVELOPERS): #noqa
		await ctx.respond("You are not allowed to run this command")
		return

	response = help_messages.about_system # Base text

	if not DISALLOW_PLATFORM_LEAKS:
		if IS_ANDROID  : response = response + "\n" + loadString("/android/command_flare")
		if IS_DEBUGGING: response = response + "\n" + loadString("/debug/command_flare")

	await ctx.respond(response, ephemeral=True)

@fritz.command(name="about", description="Learn more about Fritz")
async def sysabout(ctx):
	await ctx.respond(help_messages.about_fritz)

@fritz.command(name='invite', description='Get Fritz\'s invite URL', pass_context=True)
async def getInvite(ctx):
	await ctx.respond("NOTE: This link is to add Fritz to a SERVER. To add it to an account, you need to click \"Add App\" in Fritz's profile\n" + INVITE_URL, ephemeral=True)

@fritz.command(name='git_url', description='Get Fritz\'s Git URL')
async def getGit(ctx): await ctx.respond(GIT_URL)

### ===================================== ###
### DEVELOPER ONLY ###
@zdev.command(name="memdump")
@isDeveloper()
async def memdump(context, dump_module_contents:bool=False):
	await context.defer()

	with open(f"{PATH}/dump_{BOOTID}", "x") as dumpfile:

		print("### BEGIN MEMORY DUMP ###")
		print(globals())
		print(locals())

		print("\n\n\n")

		print(sys.modules)

		dumpfile.write(str(globals()) + "\n")
		dumpfile.write(str(locals()) + "\n")
		dumpfile.write("\n\n\n")
		dumpfile.write(str(sys.modules) + "\n")

		if dump_module_contents:
			import main
			from resources import shared
			print("module.main\n" + str(dir(main)))
			print("module.shared\n" + str(dir(shared)))

			dumpfile.write(str(dir(main)) + "\n")
			dumpfile.write(str(dir(shared)) + "\n")

		print("### END MEMORY DUMP ###")

	await context.respond("Memory dumped")

@zdev.command(name='shutdown')
@isDeveloper()
async def initiateShutdown(ctx):
	await ctx.respond(":saluting_face:")

	os.system("sudo systemctl stop fritz")

@zdev.command(name='download_messages')
@isDeveloper()
async def downloadMessages(ctx, id):
	await ctx.defer(ephemeral="True")

	messageList = await discord_fancy.query_messages(id)

	authorList  = await discord_fancy.parse_tools.messages.authors(messageList)
	contentList = await discord_fancy.parse_tools.messages.content(messageList)

	index = 0

	for author in authorList:
		print(f"{RED}CACHED: {str(id)}{YELLOW} {str(author)}: {DRIVES}{str(contentList[index])}{RESET}")
		index += 1

	await ctx.respond("Dumped to console")

### ===================================== ###
# Commands for plugins. Unfortunately must be in this file
def _psi__log(hooked, function):
	journal.log(f"[Plugin subsystem] Hook registered: {hooked}, {function.__name__}", 6)

def psi_register_on_message(function):
	global _on_message_hooks

	_psi__log("on_message", function)
	_on_message_hooks.append(function)

def psi_register_on_ready(function):
	global _on_ready_hooks

	_psi__log("on_ready", function)
	_on_ready_hooks.append(function)

def psi_register_application_command_error(function):
	global _on_application_command_error_hooks

	_psi__log("on_application_command_error", function)
	_on_application_command_error_hooks.append(function)

## Support for plug-in modules in plugins/
if ENABLE_IMPORTED_PLUGINS:
	if not os.path.exists(f"{PATH}/cache/HAS_SEEN_PLUGIN_WARNING"):

		print(RED + loadString("plugins").format(rd=RED, yl=YELLOW, pl=MAGENTA, rs=RESET) + RESET)

		wait = 0

		while wait != 60:
			fl02 = 60 - wait
			time.sleep(1)
			wait += 1

			print(RED + f"\u001b[1FFritz will start in {fl02} seconds   ")

		open(f"{PATH}/cache/HAS_SEEN_PLUGIN_WARNING", "x").close()

	# First, make sure the plugin directory exists
	if os.path.exists(f"{PATH}/plugins"):
		plugins_to_import = os.listdir(f"{PATH}/plugins")

		for module in plugins_to_import:
			# Check to make sure the file isn't blacklisted
			if os.path.isdir(f"{PATH}/plugins/{module}") or ".env" in module:
				pass

			else:
				try:
					# This is a huge security violation
					exec(open(f"{PATH}/plugins/{module}").read())

					try:
						t1, t2, t3 = _funchook()

						for hook in t1: psi_register_on_ready(hook)
						for hook in t2: psi_register_on_message(hook)
						for hook in t3: psi_register_application_command_error(hook)

						del _funchook

					except Exception:
						pass

					num_imported_plugins += 1

				except Exception as err:
					general_errors.append(f"Plugin '{module[:-3]}' failed to activate: " + str(err))

	else:
		journal.log("Plugin are enabled, but plugin directory is missing!", 4)
		general_errors.append("Plugins are enabled, but plugin directory is missing!")

### ===================================== ###

if __name__ == "__main__":
	try:
		match [IS_DEBUGGING, IS_ANDROID]:
			case [False, False]: print(MAGENTA + f"Fritz {VERSION}" + RESET)
			case [True, False] : print(MAGENTA + f"Fritz {VERSION}" + RED + " (debug mode)" + RESET)
			case [False, True] : print(MAGENTA + f"Fritz {VERSION}" + RED + " (experimental)" + RESET)
			case [True, True]  : print(MAGENTA + f"Fritz {VERSION}" + RED + " (debug, experimental)" + RESET)

		print("")

		if starboard.NOQB:
			errors_during_startup += 1

		bot.run(TOKEN)

	except Exception as err:
		print(MAGENTA + "FATAL: " + RED + "Failed to start Fritz")
		print("   -> " + str(err) + RESET)

		journal.log_fatal("Failed to start: " + str(err))
