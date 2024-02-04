import sys, os, datetime, nest_asyncio, asyncio

from types import NoneType

from threading import Thread as td
from discord.ext import commands

from resources.colour import *
from resources.shared import TOKEN, intents, ENABLE_LOGGING, LOGGING_BLACKLIST, AI_BLACKLIST, PATH, REDUCE_DISK_READS, LYRIC_BLACKLIST

import scripts.tools.logging as logging
import scripts.tools.loadHandler as loadHandler
import scripts.tools.heyFritz as heyFritz

import private.ci_private

from scripts.tools.utility import *

import resources.client_personalities as personalities

client_personality = personalities.Default.none 	

client = client_personality[0]
bot = commands.Bot(intents=intents)

loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)

cached_lyrics = str(os.listdir(sys.path[0] + "/resources/docs/lyrics"))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CheckFailure):
		await ctx.send('You don\'t have the required role')

	else:
		await ctx.send(str(error))

@client.event
async def on_ready(): 
	print(MAGENTA + "[  Main  ] " + YELLOW + "Ready with personality %s"%client_personality[1] + RESET)

@client.event
async def on_message(message):
	global cached_lyrics

	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = datetime.date.today()

	fs = str(today) + " " + str(current_time) + " "
	match [ENABLE_LOGGING, not isinstance(message.guild, NoneType)]:
		case [True, True]: 
			match message.guild.id in LOGGING_BLACKLIST:
				case False: await logging.logMessage(message)
				case True: NotImplemented

	if not REDUCE_DISK_READS: cached_lyrics = str(os.listdir(sys.path[0] + "/resources/docs/lyrics"))

	if str(message.content) == "INTERNAL_FLAG::::__update_lyrcache":
		await message.delete()
		cached_lyrics = str(os.listdir(sys.path[0] + "/resources/docs/lyrics"))
		
		log("Re-cached lyrics directory")

	match [str(message.content).lower() in cached_lyrics, str(message.author.id) != "1070042394009014303", not message.guild.id in LYRIC_BLACKLIST]:
		case [True, True, True]: 
			await heyFritz.lyricLoader(message)

	match [str(message.content).lower() == "hey fritz, panic 0x30", str(message.author.id) in registeredDevelopers]:
		case [True, True]:
			os.system("notify-send -u critical -t 2000 'Fritz' 'Panic code 0x30' --icon /home/%s/Pictures/fritzSystemIcon.jpeg -e"%os.getlogin())
			os.system("pkill /home/%s/Documents/Fritz/ -f"%os.getlogin())

	match ["hey fritz," in str(message.content).lower(), not isinstance(message.guild, NoneType), "hey fritz" in str(message.content).lower(), str(message.author.id) != "1070042394009014303"]:
		case [True, True, _, True]: # This is a guild
			match [not message.guild.id in AI_BLACKLIST]:
				case [True]: await heyFritz.onHeyFritz(message, loop)
				case [False]: await message.channel.send("That function is disabled on this server")

		case [False, _, True, True]: 
			await message.channel.send("It looks like you were trying to invoke me", silent=True); await asyncio.sleep(0.5)
			await message.channel.send("However, you did not use the correct format", silent=True); await asyncio.sleep(0.5)
			await message.channel.send("Here's an example of the correct format: `Hey Fritz, this is a cool prompt`", silent=True); await asyncio.sleep(0.5)
			await message.channel.send("You must include a comma immediately after Fritz, without a space: `Fritz,`", silent=True); await asyncio.sleep(0.5)
			await message.channel.send("Capitalisation does not matter, this is still valid: `HeY fRitZ, CoOl ProMpT`", silent=True)
		
		case [True, False, _, True]: await heyFritz.onHeyFritz(message, loop) # This is a DM or GM. Wait how did Fritz get into a GM-

	await private.ci_private.ciPrint(message, fs)

### --- Initialise the bot --- ###

loadHandler.prepBot()

def commandprocess(): os.system("python3 %s/commands_bridge.py" % PATH)

try:
	td(target=commandprocess).start()
	client.run(TOKEN)

except Exception as err:
	print(MAGENTA + "Main: " + RED + "[FATAL] - Failed to initalise base client")
	print("   -> " + str(err) + RESET)