"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

""" First-run automatic directory setup """
import scripts.hooks.firstRun

import sys, os, datetime, nest_asyncio, asyncio, json

from types import NoneType

from threading import Thread as td
from discord.ext import commands

from resources.colour import *
from resources.shared import TOKEN, intents, ENABLE_LOGGING, LOGGING_BLACKLIST, AI_BLACKLIST, PATH, IS_DEBUGGING

import scripts.tools.logging as logging
import scripts.tools.loadHandler as loadHandler

from resources.responses import help_messages

from scripts.tools.utility import *

import resources.client_personalities as personalities

if not IS_DEBUGGING: client_personality = personalities.Default.none 	
else:                client_personality = personalities.Default.debug

client = client_personality[0]
bot = commands.Bot(intents=intents)

loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send('You don\'t have the required role')

	else:
		await ctx.send(str(error))

@client.event
async def on_ready(): 
	print(MAGENTA + "[  Main  ] " + YELLOW + "Ready!" + RESET)

@client.event
async def on_message(message):
	### LOG THE MESSAGE TO THE APPROPRIATE FILE, REGARDLESS OF CONTENT ###
	if str(message.content).lower() == "all stay strong":
		await message.channel.send("We live eternally")

	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = datetime.date.today()
	fs = str(today) + " " + str(current_time) + " "

	## Log the message to the disk ##
	match [ENABLE_LOGGING, not isinstance(message.guild, NoneType)]:
		case [True, True]: 
			match message.guild.id in LOGGING_BLACKLIST:
				case False: await logging.logMessage(message)

		case [True, False]: await logging.logMessage(message)


	## If the user is banned, no code past this point should run ##
	if message.author.id in BLACKLISTED_USERS:
		return


	### ============================================================= ###
	## Panic exit ##
	match [str(message.content).lower() == "hey fritz, panic 0x30", str(message.author.id) in registeredDevelopers]:
		case [True, True]:
			os.system("notify-send -u critical -t 2000 'Fritz' 'Panic code 0x30' --icon /home/%s/Pictures/fritzSystemIcon.jpeg -e"%os.getlogin())
			os.system("pkill /home/%s/Documents/Fritz/ -f"%os.getlogin())


	## Hey Fritz invocation ##
	if "hey fritz," in str(message.content).lower(): await message.channel.send(help_messages.MACHINE_LEARNING_NOTICE)


### --- Initialise the bot --- ###

loadHandler.prepBot()

def commandprocess(): os.system("python3 %s/commands_bridge.py" % PATH)

# Do a cheeky little advertisement #
if not os.path.exists(PATH + "/cache/gabrielPrompt"):
	print(YELLOW + "If you're using Fritz primarily for logging, you should migrate to Gabriel" + RESET)
	print(MAGENTA + "You can find Gabriel at https://github.com/psychon-night/Gabriel-for-Discord" + RESET)
	os.system(f"touch {PATH}/cache/gabrielPrompt")

try:
	if IS_DEBUGGING: print(RED + "Overriding selected personality (debug flag set to True)" + RESET)
	if not client_personality[1] == "none": print(MAGENTA + "Starting with personality %s"%client_personality[1] + RESET)
	else: print(MAGENTA + "Starting with no personality" + RESET)
	td(target=commandprocess).start()
	client.run(TOKEN)

except Exception as err:
	print(MAGENTA + "[  Main  ] " + RED + "Failed to start main process")
	print("   -> " + str(err) + RESET)
	print(YELLOW + "Logging, Hey Fritz, and panic codes are unavailable" + RESET)
