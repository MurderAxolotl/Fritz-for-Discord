"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

""" First-run automatic directory setup """
import scripts.hooks.firstRun

import os
import asyncio
import nest_asyncio

from threading import Thread as td
from discord.ext import commands

from resources.colour import *
from resources.shared import TOKEN, intents, PATH, IS_DEBUGGING, IS_ANDROID, version

import scripts.tools.loadHandler as loadHandler

from resources.responses import help_messages

from scripts.tools.utility import *

import resources.client_personalities as personalities

if not IS_DEBUGGING: client_personality = personalities.Holiday.spooky
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
async def on_ready(): print(MAGENTA + "[  Main  ] " + YELLOW + "Ready!" + RESET)

@client.event
async def on_message(message):
	if str(message.content).lower() == "all stay strong": await message.channel.send("We live eternally")

	## If the user is banned, no code past this point should run ##
	if message.author.id in BLACKLISTED_USERS: return


	### ============================================================= ###
	## Panic exit ##
	match [str(message.content).lower() == "hey fritz, panic 0x30", str(message.author.id) in registeredDevelopers]:
		case [True, True]:
			os.system("notify-send -u critical -t 2000 'Fritz' 'Panic code 0x30' --icon /home/%s/Pictures/fritzSystemIcon.jpeg -e"%os.getlogin())
			os.system("pkill /home/%s/Documents/Fritz/ -f"%os.getlogin()) # I need to fix this


### --- Initialise the bot --- ###

loadHandler.prepBot()

def commandprocess(): os.system("python3 %s/commands_bridge.py" % PATH)

# Do a cheeky little advertisement #
if not os.path.exists(PATH + "/cache/gabrielPrompt"):
	print(YELLOW + "If you're using Fritz primarily for logging, you should migrate to Gabriel" + RESET)
	print(MAGENTA + "You can find Gabriel at https://github.com/psychon-night/Gabriel-for-Discord" + RESET)
	os.system(f"touch {PATH}/cache/gabrielPrompt")

try:
	print(MAGENTA + f"Fritz {version}" + RESET)

	if IS_DEBUGGING: print(RED + loadString("/debug/startup_flare") + RESET)
	if IS_ANDROID: print(RED + loadString("/android/startup_flare") + RESET)
	
	td(target=commandprocess).start()
	client.run(TOKEN)

except Exception as err:
	print(MAGENTA + "[  Main  ] " + RED + "Failed to start main process")
	print("   -> " + str(err) + RESET)
	print(YELLOW + "Logging, Hey Fritz, and panic codes are unavailable" + RESET)
