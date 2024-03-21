import asyncio
import nest_asyncio

from resources.curl_requests import *
from resources.shared import *
from resources.responses import *
from resources.colour import *
from resources.user_messages import *

import scripts.api.qrTools as qrTools
import scripts.api.oneoff as oneOff
import scripts.api.gpt as gpt
import scripts.api.pronouns as pronouns
import scripts.api.spotify as spotify
import scripts.api.characterAI as cai
import scripts.api.discord as discord_fancy
import scripts.errors.commandCheck as commandCheck

import scripts.tools.lyricLoader as keyphrase

import scripts.hooks.commandsEverywhere as ceMixin

from scripts.tools.utility import *

bot = discord.Bot()
loop = asyncio.get_event_loop()
nest_asyncio.apply(loop)

### COMMAND GROUPS ###
fritz = bot.create_group("f", "Fritz command group")
inDev = bot.create_group("f_unstable", "Unstable and under development")
qr    = bot.create_group("qr", "Tools relating to QR codes")
kw    = bot.create_group("phrase", "Tools relating to reaction phrases")
zdev  = bot.create_group("f_dev", "Developer-only utilities")


### ===================================== ###
### EVENTS ###
@bot.event	
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException): await commandCheck.on_command_error(ctx, error)
				
@bot.event
async def on_ready(): 
	print(MAGENTA + "[Commands]" + YELLOW + " Ready!" + RESET)
	# await ceMixin.hook()

	

### ===================================== ###
## API COMMANDS ##

# @audio.command(name="voice_bridge", description='Bridge two voice channels together')
# async def initSync(ctx, vc_id_1, vc_id_2): await voiceLink.bridgeVoiceChannels(ctx, bot, vc_id_1, vc_id_2)

# Search PronounsPage for a user #
@fritz.command(name="pp_users", description='Search PronounsPage for a user', pass_context=True)
async def pronounspage(ctx, query:str): await pronouns.pp_searchUser(ctx, query)

# Search PronounsPage for a term #
@fritz.command(name="pp_terms", description='Search PronounsPage for a tern', pass_context=True)
async def pronounspage(ctx, query:str): await pronouns.pp_searchTerms(ctx, query)

# SEARCH SPOTIFY #
@fritz.command(name="seasify", description='Search Spotify for a song', pass_context = True)
async def seasify(ctx, query:str, count:int=10): await spotify.searchSpotify(ctx, query, count)

## Chat Completion ##
@fritz.command(name='assistant', description='Launch Fritz\'s AI assistant', pass_context=True) # Async
async def chatgpt(ctx, prompt:str, legacy_mode:discord.Option(str, choices=gpt.LEGACY_MODES, description="Legacy mode select")="none"): await gpt.generateResponse(ctx, prompt, loop, legacy_mode) #type:ignore

# CHARACTER AI #
@fritz.command(name="cai", description='Give Fritz an identity crisis', pass_context = True)
async def cget(ctx, message:str, character:discord.Option(str, choices=cai.CHARACTERS.keys(), description='Character to interact with'), reset:discord.Option(bool, choices=[True, False],description='Set to true to erase chat history')=False): await cai.doTheThing(ctx, message, character, reset) #type:ignore

### ===================================== ###
## QR CODES ##

# SCAN A QR CODE #
@qr.command(name="scan", description="Scan a QR code", pass_context=True)
async def scanQR(ctx, qr_image_url): await qrTools.read(ctx, qr_image_url)

# CREATE A QR CODE #
@qr.command(name="create", description="Make a QR code", pass_context=True)
async def makeQR(ctx, qr_data, style_mode:discord.Option(str, choices=qrTools.designTypes, description='QR style')="stylized (default)"): #type:ignore
	await qrTools.createQR(ctx, qr_data, style_mode)

### ===================================== ###
## KEYPHRASES ##
	
@kw.command(name="create", description="Create a reaction phrase ")
async def createRP(ctx, trigger_phrase, response): await ctx.respond(await keyphrase.createKeyword(ctx, trigger_phrase, response))

@kw.command(name="delete", description="Delete a reaction phrase ")
async def createRP(ctx, trigger_phrase): await ctx.respond(await keyphrase.deleteKeyword(ctx, trigger_phrase))

@kw.command(name="read", description="Read the contents of a reaction phrase ")
async def createRP(ctx, trigger_phrase): await ctx.respond(await keyphrase.readKeyword(trigger_phrase))

@kw.command(name="edit", description="Edit the contents of a reaction phrase ")
async def createRP(ctx, trigger_phrase, new_content): await ctx.respond(await keyphrase.editKeyword(trigger_phrase, new_content))

@kw.command(name="list", description="List all reaction phrases")
async def createRP(ctx): await ctx.respond(await keyphrase.listKeywords())

### ===================================== ###
## FUN ##

# CAT PICTURE #
@fritz.command(name="givecat", description="Get a random cat photo")
async def givecat(ctx): await oneOff.giveCat(ctx)

# GET A JOKE #
@fritz.command(name="joke", description="Grab a random joke from the :sparkles: internet :sparkles:", pass_context = True)
async def joke(ctx): await oneOff.getRandomJoke(ctx)

# GET A QUOTE #
@fritz.command(name="quote", description="Grab a random quote from the :sparkles: internet :sparkles:")
async def quote(ctx): await oneOff.getRandomQuote(ctx)

# QUOTE URSELF #
@fritz.command(name="quoteme", description="Get a random quote from yourself")
async def qm(ctx, username:str=None): await oneOff.quoteMe(ctx, username)

### ===================================== ###
## USER MANAGEMENT ##


### ===================================== ###
## BOT UTILITIES ##
@fritz.command(name='ping', description='Get Fritz\'s current ping', guild_only=False)
async def ping(ctx):
	latency = round(bot.latency * 1000); await ctx.respond('Current latency: ' + str(latency) + "ms")

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
@isDeveloper()
async def help(ctx): await ctx.respond(help_messages.about_system, ephemeral=True)

@fritz.command(name='invite', description='Get Fritz\'s invite URL', pass_context=True)
async def getInvite(ctx): 
	await ctx.respond(INVITE_URL, ephemeral=True)

@fritz.command(name='github_url', description='Get Fritz\'s Github URL')
async def getGit(ctx): await ctx.respond(GIT_URL)

### ===================================== ###
## DEVELOPER ONLY ## 
	
@fritz.command(name='initiate_dm', description="Initiates a DM with the current user")
async def do(ctx): 
	await ctx.author.send("Hey! I'm Fritz, your friendly assistant! How can I help you?")
	await ctx.author.send("Remember: you can ask me anything. Just say: `Hey Fritz, it's nice to meet you!`")
	await ctx.author.send("You can also use the *assistant* slash command")

	await ctx.respond("DM created", ephemeral=True)

@zdev.command(name='shutdown', description='fritz.dev.shutdown', pass_context=True)
@isDeveloper()
async def initiateShutdown(ctx):
	await ctx.respond(":saluting_face:")
	os.system("notify-send -u critical -t 2000 'Fritz' 'A shutdown has been initiated' --icon %s/fritzSystemIcon.jpeg -e"%PATH)
	os.system("pkill %s -f"%PATH)

@zdev.command(name='download_messages', description='fritz.dev.download_messages')
@isDeveloper()
async def downloadMessages(ctx, id):
	await ctx.defer()

	messageList = await discord_fancy.query_messages(id)

	authorList  = await discord_fancy.parse_tools.messages.authors(messageList)
	contentList = await discord_fancy.parse_tools.messages.content(messageList)

	index = 0

	for author in authorList:
		print(f"{RED}CACHED: {str(id)}{YELLOW} {str(author)}: {DRIVES}{str(contentList[index])}{RESET}")
		index += 1

	await ctx.respond("Dumped to console")

### ===================================== ###

try:
	bot.run(TOKEN)

except Exception as err:
	print(MAGENTA + "[Commands] " + RED + "Failed to start slash command features")
	print("   -> " + str(err) + RESET)
	print(YELLOW + "Slash commands are unavailable" + RESET)