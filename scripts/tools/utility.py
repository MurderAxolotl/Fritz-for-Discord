"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import os, asyncio, requests
import discord, datetime, sys
from discord.ext import commands
from resources.colour import *

from resources.shared import PATH

from resources.shared import BLACKLISTED_USERS, registeredDevelopers

from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

loop = asyncio.get_event_loop()

async def check(ctx):
	""" Check if the current message instance is a DM. Returns true if this is a DM, false if this is a guild """
	if isinstance(ctx.channel, discord.channel.DMChannel): return True
	else: return False

def log(input):
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = datetime.date.today()

	logPath = sys.path[0] + "/logs/system.log"

	with open(logPath, "a") as output_log:
		output_log.write("")

class bannedFromNSFW(commands.CheckFailure): NotImplemented
class swiperNoSwipingError(commands.CheckFailure): NotImplemented
class bannedUser(commands.CheckFailure): pass
class aprilfools(commands.CheckFailure): pass

### CUSTOM COMMAND CHECK PREDICATES ###

def swiperNoSwiping():
	async def predicate(ctx):
		if not await ctx.bot.is_owner(ctx.author): raise swiperNoSwipingError("Swiper no Swiping")
		return True
	
	return commands.check(predicate)

def isDeveloper():
	async def predicate(ctx):
		if not str(ctx.author.id) in registeredDevelopers: raise commands.NotOwner
		
		return True
		
	
	return commands.check(predicate)

## Misc utilities ## 

async def downloadYoutubeVideo(video_url, id):
	string = 'yt-dlp "' + video_url + '" -x -q -N 25 -o video_cache' + str(id) + " --path /home/%s/Documents/Fritz/cache"%os.getlogin()

	await loop.run_in_executor(ThreadPoolExecutor(), lambda: os.system(string))
	os.system("rm /home/%s/Documents/Fritz/*.webm 2> /dev/null"%os.getlogin())

async def getPageTitle(URL):
	try:
		pageGet = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(URL))
		soup = BeautifulSoup(pageGet.text, 'html.parser')

		return str(soup.find('title')).replace("<title>", "").replace("</title>", "").replace(" - YouTube", "")
	
	except Exception as err: 
		print(str(err)); return "UNKNOWN"

async def depricatedCommand(ctx):
	""" Sends a depricated command warning """
	await ctx.channel.send("NOTE: This command is depricated and will be removed in an upcoming release")

# This should not be async. I don't want it to be async. I don't care if it causes blockages.
def loadString(stringFile:str) -> str:
	""" Loads a string from the disk and returns it
	
	Strings are stored in /resources/strings """

	BASE = PATH + "/resources/strings"

	try:
		file = open(f"{BASE}/{stringFile}.tout", "r")

		contents = file.read()
		file.close()

		return contents
	
	except FileNotFoundError:
		print(RED + f"ERR: FILE {MAGENTA}{stringFile}{RED} NOT FOUND. RETURNING AN EMPTY STRING TO AVOID CRASH." + RESET)
		return ""
	
	except Exception as err:
		print(RED + f"ERR: FAILED TO READ {MAGENTA}{stringFile}{RED}: {str(err)}" + RESET)

		return ""
