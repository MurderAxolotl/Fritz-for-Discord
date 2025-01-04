import asyncio

from io import StringIO

from concurrent.futures import ThreadPoolExecutor

from discord.ext import commands

from resources.curl_requests import *
from resources.shared import *
from resources.responses import *
from resources.colour import *

import scripts.api.gpt as gpt
import scripts.api.midjourney as midjourney
import scripts.api.pronouns as pronouns
import scripts.api.spotify as spotify
import scripts.errors.commandCheck as commandCheck

from scripts.tools.utility import *


bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
loop = asyncio.get_event_loop()


### ===================================== ###
### EVENTS ###

@bot.event
async def on_command_error(ctx, error): await commandCheck.on_command_error(ctx, error)
				
@bot.event
async def on_ready(): print(MAGENTA + "[Commands] " + YELLOW + "Ready!" + RESET)

### ===================================== ###
## API COMMANDS ##

@bot.command(name="pp_users", description='Search PronounsPage for a user', pass_context=True)
async def pronounspage(ctx, query): await pronouns.pp_searchUser(ctx, query)

@bot.command(name="pp_terms", description='Search PronounsPage for a tern', pass_context=True)
async def pronounspage(ctx, query): await pronouns.pp_searchTerms(ctx, query)

@bot.command(name='chatgpt', description='talk to fritz', pass_context=True) # Async
async def chatgpt(ctx, prompt): await gpt.generateResponse(ctx, prompt, loop, model="text-davinci-003")

@bot.command(name='mj', description='generate with midjourney', pass_context=True) # Async
async def mj2(ctx, prompt, mode='realistic'): await midjourney.generateFromPrompt(ctx,prompt,mode)

@bot.command(name="seasify", pass_context = True)
async def seasify(ctx, query, count=10): await spotify.searchSpotify(ctx, query, count)


### ===================================== ###
## TOOLS ##
	 

### ===================================== ###
## USER MANAGEMENT ##


### ===================================== ###
## BOT UTILITIES ##

@bot.command(name='ping', description='get the bot\'s current ping', pass_context=True)
async def ping(ctx):
	latency = round(bot.latency * 1000)

	await deleteMessage(ctx)
	await ctx.channel.send('Current latency: ' + str(latency) + "ms")


### ===================================== ###
## INFORMATION COMMANDS ##


@bot.command(name="help", description="stop it. get some help.", pass_context=True)
async def help(ctx): await deleteMessage(ctx); await ctx.send(help_messages.commands)

## Get basic info about Fritz ##
@bot.command(name="about", description="list basic info about Fritz", pass_context=True)
async def help(ctx): await deleteMessage(ctx); await ctx.send(help_messages.about)

## Get advanced info about Fritz ##
@bot.command(name="system", description="list advanced info about Fritz", pass_context=True)
async def help(ctx): await deleteMessage(ctx); await ctx.send(help_messages.about_system)


@bot.command(name='invite', description='get invite url', pass_context=True)
async def getInvite(ctx): await deleteMessage(ctx); await ctx.send("Here ya go!"); await ctx.send(INVITE_URL)


### ===================================== ###

try:
	# loop.run_until_complete(main())
	bot.run(TOKEN)

except Exception as err:
	print(MAGENTA + "Commands: " + RED + "[FATAL] - Unable to create instance of command processor")
	print("   -> " + str(err) + RESET)
	os.abort()
