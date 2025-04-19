###############################################################################
# ASSUMES THERE'S A MINECRAFT SERVER RUNNING UNDER THE SAME PUBLIC IP ADDRESS #
###############################################################################

import os, sys, requests, json
from datetime import datetime

from resources.shared import MINECRAFT_SERVER_PORT, LIMIT_MCSTATUS_COMMAND, ALLOWED_MCSTATUS_SERVERS, MINECRAFT_SERVER_FIXED_ADDRESS

ENDPOINT = "https://api.mcsrvstat.us/3"

# LIVE_IP = requests.get('https://api.ipify.org').content.decode('utf8')
LIVE_IP = MINECRAFT_SERVER_FIXED_ADDRESS
IP = f"{LIVE_IP}:{MINECRAFT_SERVER_PORT}"

def unixToISO(unix_timestamp:int):
	return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S') #type:ignore Does it look like I give a shit if this is depricated?

async def getServerStatus(ctx, sendPlayerList=False):
	await ctx.defer()

	# Check if the command can even run here
	if LIMIT_MCSTATUS_COMMAND:
		try: SERVER_ID = str(ctx.guild.id)
		except:
			# Not in a server, not allowed
			await ctx.respond("This command cannot be used here")
			return
		
		if not SERVER_ID in ALLOWED_MCSTATUS_SERVERS:
			await ctx.respond("This command cannot be used in this server")
			return

	# Blocking call, too lazy to make it async
	apiResponse = requests.get(f"{ENDPOINT}/{IP}")
	responseJSON = json.loads(apiResponse.text)

	# Parse out response info
	ONLINE = responseJSON["online"] # Is the server online?
	CACHED = responseJSON["debug"]["cachehit"]
	CACHE_EXPIRE = responseJSON["debug"]["cacheexpire"]
	CACHE_EXPIRE_ISO = unixToISO(CACHE_EXPIRE)

	if ONLINE: 
		PLAYERS_ONLINE = responseJSON["players"]["online"]
		PLAYERS_MAX = responseJSON["players"]["max"]

	else:
		PLAYERS_ONLINE = "?"
		PLAYERS_MAX = "?"

	# Dynamic string goodness
	CACHE_TEXT = "-# Info is up-to-date and not cached" if not CACHED else f"-# Info may be out of date. Cache expires at {CACHE_EXPIRE_ISO}"
	PLAYER_TEXT = f"{PLAYERS_ONLINE} online / {PLAYERS_MAX} max"

	if ONLINE:

		if sendPlayerList:
			# Build the string list of players
			detectedPlayers = ""

			for playerInstance in responseJSON["players"]["list"]:
				if detectedPlayers == "": detectedPlayers = playerInstance["name"]
				else: detectedPlayers = detectedPlayers + ", " + playerInstance["name"]
				
			if detectedPlayers != "": detectedPlayers = "\n" + detectedPlayers

		else: detectedPlayers = ""

		await ctx.respond(f"Server is online!\nIP: `{IP}`\nPlayers: {PLAYER_TEXT}{detectedPlayers}\n\n{CACHE_TEXT}", ephemeral=True)

	else:
		await ctx.respond(f"Server is offline!\nIP: `{IP}`\n{CACHE_TEXT}", ephemeral=True)