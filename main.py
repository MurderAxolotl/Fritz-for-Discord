import sys, os, datetime
import nest_asyncio, asyncio

from threading import Thread as td
from discord.ext import commands

from resources.colour import *
from resources.shared import TOKEN, intents

import scripts.tools.utility as utility
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
	unit = None

	if await utility.check(message) == True: 
		guild_id = str(message.author).split("#0", 1)[0]; unit = "users"
		logPath = sys.path[0] + "/logs/%s/%s.log"%(unit, guild_id)

	else: 
		try: guild_id = str(message.guild.id)
		except: guild_id = 0; print(RED + "Guild cache needs to be refreshed" + RESET)
		channel_id = str(message.channel.id)

		logPath = sys.path[0] + "/logs/guilds/%s/%s.log"%(guild_id, channel_id)

		if not os.path.isdir(sys.path[0] + "/logs/guilds/%s"%(guild_id)):
			print(YELLOW + "Creating dir %s"%sys.path[0] + "/logs/guilds/%s"%(guild_id))
			os.mkdir(sys.path[0] + "/logs/guilds/%s"%(guild_id))

	# if ":3" in str(message.content) or "colon" in str(message.content).lower() or ":" in str(message.content) or "3" in str(message.content): 
	# 	if not str(message.author.id) == "1063584978081951814": await message.delete()
	if "ugly" in str(message.content).lower().replace(" ", ""): await message.delete()

	if guild_id == "1170869996856016956":
		if str(message.channel.id) == "1170871176638246962":
			print("Message detected in #da-rules")
			if not (str(message.author.id) == "805166021752520714") and not str(message.author.id) == "1150602405755502723":
				print("Message not authorized")
				await message.delete()

	fs = str(today) + " " + str(current_time) + " "
	messageContent = str(message.author).split("#0")[0] + ": " + message.content

	if (os.path.isfile(logPath)): log = open(logPath, "a")
	else: log = open(logPath, "+x")

	log.write(fs + messageContent + "\n")
	log.close()

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