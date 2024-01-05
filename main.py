import sys, os, datetime
import nest_asyncio, asyncio

from threading import Thread as td
from discord.ext import commands

from resources.colour import *
from resources.shared import TOKEN, intents, AUTHORISED_DEVELOPERS

import scripts.tools.logging as logging
import scripts.tools.loadHandler as loadHandler

import resources.client_personalities as personalities
from scripts.tools.utility import *

PATH = sys.path[0]

client_personality = personalities.Default.standard 	

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
async def on_ready(): print(MAGENTA + "[Main] " + YELLOW + "Ready with personality %s"%client_personality[1] + RESET)

@client.event
async def on_message(message):
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = datetime.date.today()

	fs = str(today) + " " + str(current_time) + " "

	logging.logMessage(message)

	if str(message.content).lower() == "hey fritz, panic 0x30":
		if str(message.author) in AUTHORISED_DEVELOPERS:
			os.system("notify-send -u critical -t 2000 'Fritz' 'Panic code 0x30' --icon /home/%s/Pictures/fritzSystemIcon.jpeg -e"%os.getlogin())
			os.system("pkill /home/%s/Documents/Fritz/ -f"%os.getlogin())

	if str(message.guild.id) == "1064071365449228338":
		print(MAGENTA + SEAFOAM + fs + str(message.channel.id) + YELLOW + " " + str(message.author).split("#0")[0] + DRIVES + ": " + str(message.content) + RESET)


### --- Initialise the bot --- ###

loadHandler.prepBot()

def commandprocess(): os.system("python3 %s/commands_bridge.py" % os.getcwd())

try:
	td(target=commandprocess).start()
	client.run(TOKEN)

except Exception as err:
	print(MAGENTA + "Main: " + RED + "[FATAL] - Unable to create instance of main")
	print("   -> " + str(err) + RESET)
	os.abort()