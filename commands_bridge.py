import asyncio
import time
import nest_asyncio

from discord.ext import bridge

from resources.curl_requests import *
from resources.shared import *
from resources.responses import *
from resources.colour import *
from resources.user_messages import *

import scripts.tools.darkNights as darkNights
import scripts.tools.audioCommands_multimem as audioCommands
# import _oldCode.audioCommands as audioCommands

import scripts.api.qrTools as qrTools
import scripts.api.oneoff as oneOff
import scripts.api.gpt as gpt
import scripts.api.midjourney as midjourney
import scripts.api.stablediffusion as stableDiffusion
import scripts.api.pronouns as pronouns
import scripts.api.spotify as spotify
import scripts.api.characterAI as cai
import scripts.errors.commandCheck as commandCheck

from scripts.tools.utility import *


bot = discord.Bot()
loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)

### COMMAND GROUPS ###
fritz = bot.create_group("f", "Fritz command group")
inDev = bot.create_group("f_unstable", "Unstable and under development")
zdev = bot.create_group("f_dev", "Developer-only utilities")
audio = bot.create_group("audio", "Audio tools")


### ===================================== ###
### EVENTS ###

@bot.event	
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException): await commandCheck.on_command_error(ctx, error)
				
@bot.event
async def on_ready(): print(MAGENTA + "[Commands]" + YELLOW + " Ready!" + RESET)

### ===================================== ###
## API COMMANDS ##
## Generic APIs ##
# Search PronounsPage for a user #
@fritz.command(name="pp_users", description='Search PronounsPage for a user', pass_context=True)
async def pronounspage(ctx, query:str): await pronouns.pp_searchUser(ctx, query)

# Search PronounsPage for a term #
@fritz.command(name="pp_terms", description='Search PronounsPage for a tern', pass_context=True)
async def pronounspage(ctx, query:str): await pronouns.pp_searchTerms(ctx, query)

# SCAN A QR CODE #
@fritz.command(name="scan_qr", description="Scan a QR code", pass_context=True)
async def scanQR(ctx, qr_image_url): await qrTools.read(ctx, qr_image_url)

# CREATE A QR CODE #
@fritz.command(name="create_qr", description="Make a QR code", pass_context=True)
async def makeQR(ctx, qr_data, style_mode:discord.Option(str, choices=qrTools.designTypes, description='QR style')="stylized (default)"): 
	await qrTools.createQR(ctx, qr_data, style_mode)

# SEARCH SPOTIFY #
@fritz.command(name="seasify", description='Search Spotify for a song', pass_context = True)
async def seasify(ctx, query:str, count:int=10): await spotify.searchSpotify(ctx, query, count)

## MIDJOURNEY ##
@fritz.command(name='mj', description='Generate with Midjourney', pass_context=True) # Async
async def mj2(ctx, prompt:str, style:discord.Option(str, choices=midjourney.modeKeys.keys(), description='What artstyle to use')='realistic'): 
	await midjourney.generateFromPrompt(ctx,prompt,style)

# STABLE DIFFUSION #
@fritz.command(name='diffuse', description='Generate with Stable Diffusion', pass_context=True) # Async
async def stableDiffuse(ctx, prompt:str, count:int=1): await stableDiffusion.doGen(ctx, prompt, count)

# NSFW ART GENERATION #
@fritz.command(name='goodporn', description='Generate NSFW artwork', pass_context=True, nsfw=True) # Async
@allowedNSFW()
async def stableDiffuse(ctx, prompt:str, style:discord.Option(str, choices=midjourney.nsfw_modeKeys.keys(), description='What artstyle to use')='hd_realism'): 
	await midjourney.nsfwGenerate(ctx, prompt, style)

## Chat Completion ##
@fritz.command(name='chatgpt', description='Use ChatGPT', pass_context=True) # Async
async def chatgpt(ctx, prompt:str): await gpt.generateResponse(ctx, prompt, loop)

#@zdev.command(name="clyde", description="dev.clyde.copycat")
#async def doClyde(ctx, prompt): await clyde.doClydeShit(ctx, prompt)

# CHARACTER AI #
@fritz.command(name="cai", description='Give Fritz an identity crisis', pass_context = True)
async def cget(ctx, message:str, character:discord.Option(str, choices=cai.CHARACTERS.keys(), description='Character to interact with'), reset:discord.Option(bool, choices=[True, False],description='Set to true to erase chat history')=False): await cai.doTheThing(ctx, message, character, reset)

## Fun APIs ##
# CAT PICTURE #
@fritz.command(name="givecat", description="Get a random cat photo", pass_context = True)
async def givecat(ctx): await oneOff.CASS(ctx)

# GET A JOKE #
@fritz.command(name="joke", description="Grab a random quote from the :sparkles: internet :sparkles:", pass_context = True)
async def joke(ctx): await oneOff.getRandomJoke(ctx)

### ===================================== ###
## QUOTEBOOK ##
# DARK NIGHTS QUOTES #
# @fritz.command(name="dark_nights", description='Grab a randomly-selected quote from Dark Nights', pass_context = True)
# async def dnQuote(ctx, count:int=1): await darkNights.getQuote(ctx, count)

### ===================================== ###
## TOOLS ##
# Check current NSFW access level
@fritz.command(name="check_nsfw_allowed", description='Check if you can use NSFW commands in this server', pass_context = True)
async def checkNSFWAccess(ctx): 
	await ctx.send("NSFW content is allowed on this server" if manCheckAllowedNSFW(ctx) == True else "NSFW content is not allowed on this server")
	 

### ===================================== ###
## USER MANAGEMENT ##


### ===================================== ###
## BOT UTILITIES ##
@fritz.command(name='ping', description='Get Fritz\'s current ping', pass_context=True)
async def ping(ctx):
	latency = round(bot.latency * 1000); await ctx.respond('Current latency: ' + str(latency) + "ms")

### ===================================== ###
## AUDIO PLAYER ##
@audio.command(name="play", description="Plays audio from supported websites in a VC", pass_context=True)
async def pad(ctx: discord.ApplicationContext, audio_link, channel_id): await audioCommands.playAudio(ctx, audio_link, channel_id, False, bot)

@audio.command(name="queue", description="Add something to the queue", pass_context=True)
async def addQueue(ctx: discord.ApplicationContext, audio_link): await audioCommands.addQueue(ctx, audio_link)

@audio.command(name="delete_queue_item", description="Remove something from the queue. queue_item_number must be a number larger than zero, or -1 for all")
async def removeQueue(ctx, queue_item_number:int): await audioCommands.removeQueue(ctx, queue_item_number)

@audio.command(name="get_queue", description="Get the current queue", pass_context=True)
async def getQueue(ctx): await audioCommands.getQueue(ctx)

@audio.command(name="disconnect_when_done", description="Set Fritz to disconnect after the queue finishes", pass_context=True)
async def getQueue(ctx): await audioCommands.allowLeave(ctx)

@audio.command(name="pause_play", description="Basically a pause/play button")
async def togglePause(ctx): await audioCommands.pauseToggle(ctx)

@audio.command(name="skip", description="Skip current track")
async def skipTrack(ctx): await audioCommands.stopTrack(ctx)

@audio.command(name="disconnect", description="Disconnect immediately")
async def disconnectNow(ctx): await audioCommands.immediateLeave(ctx)

@audio.command(name="debug", description="Load FEAD")
async def loadFEAD(ctx): await audioCommands.getDebugInfo(ctx)

# @audio.command(name="raw_packet", description="Send raw packets of audio instead of a stream. Auto-pauses active streams")
# async def sendRawPacket(ctx, data:str="", count:int=25, autopause:discord.Option(bool, choices=[True, False])=True): await audioCommands.rawPacket(ctx, count, autopause, data)

@audio.command(name="test_socket", description="Don't use this; it's for debugging")
async def sendSocketTest(ctx): await audioCommands.audioSocketSyncTest(ctx)

@audio.command(name="audio_test", description="Don't use this; it's for debugging")
async def audioTest(ctx): await audioCommands.debugMode(ctx, bot)

### ===================================== ###
## INFORMATION COMMANDS ##
@fritz.command(name="help", description="Stop and RTFM", pass_context=True)
async def help(ctx): await ctx.respond(help_messages.commands, ephemeral=True)

@fritz.command(name="changelog", description="See recent and past changes to Fritz", pass_context=True)
async def changelog(ctx): await ctx.respond(help_messages.changelog, ephemeral=True)

## Get basic info about Fritz ##
@fritz.command(name="about", description="Get some pretty basic info about Fritz", pass_context=True)
async def help(ctx): await ctx.respond(help_messages.about, ephemeral=True)

## Get advanced info about Fritz ##
@fritz.command(name="system", description="Advanced system info", pass_context=True)
async def help(ctx): await ctx.respond(help_messages.about_system, ephemeral=True)

@fritz.command(name='invite', description='Get Fritz\'s invite URL', pass_context=True)
async def getInvite(ctx): await ctx.respond(INVITE_URL, ephemeral=True); print(bot.get_guild(ctx.guild.id))


@fritz.command(name='crazy')
async def gwazyt(ctx):
	await ctx.send("Crazy?")
	await ctx.send("I was crazy once")
	await ctx.send("They locked me in a room")
	await ctx.send("A rubber room")
	await ctx.send("A rubber room with rats")
	await ctx.send("And rats make me crazy")

@isDeveloper()
@zdev.command(name='echo')
async def gwaz(ctx, lel): await ctx.send(lel)

### ===================================== ###
## DEVELOPER ONLY ##

@zdev.command(name='trigger_update_warn', description='fritz.dev.trigger_update_warn', pass_context=True)
@isDeveloper()
async def triggerUpdateWarn(ctx): await ctx.respond(migrateToSlashCommands)

@zdev.command(name='final_migration_warning', description='fritz.dev.final_migration_warning', pass_context=True)
@isDeveloper()
async def triggerUpdateWarn(ctx): await ctx.respond(final_migration_warning)

@zdev.command(name='shutdown', description='fritz.dev.shutdown', pass_context=True)
@isDeveloper()
async def initiateShutdown(ctx):
	await ctx.respond(":saluting_face:")
	os.system("notify-send -u critical -t 2000 'Fritz' 'A shutdown has been initiated' --icon /home/%s/Pictures/fritzSystemIcon.jpeg -e"%os.getlogin())
	os.system("pkill /home/%s/Documents/Fritz/ -f"%os.getlogin())

@zdev.command(name="swiper_no_swiping", description='fritz.dev.swiper_no_swiping', pass_context=True)
@isDeveloper()
async def delete(ctx, mid): 
	await ctx.defer(ephemeral=True)
	try:
		deleteTarget = await ctx.fetch_message(mid)
		await deleteTarget.delete()
	except: ctx.respond("Invalid MID")

	aaa = await ctx.respond("Done", ephemeral=True)
	await aaa.delete()

### ===================================== ###

try:
	bot.run(TOKEN)

except Exception as err:
	print(MAGENTA + "Commands: " + RED + "[FATAL] - Unable to create instance of command processor")
	print("   -> " + str(err) + RESET)
	os.abort()
