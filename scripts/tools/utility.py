import os, asyncio, requests
import discord, datetime, sys
from discord.ext import commands
from resources.colour import *

from resources.shared import BLACKLISTED_USERS, registeredDevelopers

from discord.ext.bridge import BridgeContext
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

