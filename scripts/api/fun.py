"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import urllib.parse
import requests, asyncio, json, sys, random, discord, urllib

from concurrent.futures import ThreadPoolExecutor
from types import NoneType

from resources.colour import *
from resources.shared import QUOTE_WEBHOOK

from PIL import Image
import base64, base64, os
from io import BytesIO

loop = asyncio.get_event_loop()

async def quotebookMessage(ctx, message:str, author_id:str, author_name:str, aurl:str):
	await ctx.defer()

	form = {
		"content": f"<@{author_id}>: {message}",
		"username": f"{author_name}",
		"avatar_url": f"{aurl}"
	}

	print(requests.post(QUOTE_WEBHOOK, json = form).text)

	await ctx.respond("Quotebooked", ephemeral=True)

async def getRandomJoke(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://official-joke-api.appspot.com/jokes/random"))
	jload = json.loads(response.text)
	setup = jload["setup"]
	punchline = jload["punchline"]

	await ctx.respond("%s %s"%(setup, punchline))

async def getRandomQuote(ctx):
	keepgoing = 0
	fails = 0

	while keepgoing != 1 and fails < 6:
		try:
			response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.quotable.io/quotes?limit=40&page=%s"%random.randint(1,25)))
			
			quotes = json.loads(response.text)
			await ctx.respond(quotes["results"][random.randint(0,40)]["content"])
			
			return 0

		except Exception as err:
			print(RED + f"Unable to reach quotes API: {str(err)}" + RESET)
			fails += 1

	await ctx.respond("Quote API refused to connect")


async def quoteMe(ctx, uname):
	with ctx.typing():

		if isinstance(ctx.guild, NoneType): await ctx.respond("Must be in a guild"); return

		allc = []

		for file in os.listdir(sys.path[0] + f"/logs/guilds/{str(ctx.guild.id)}"):
			allc.append(file)

		channel = allc[random.randint(0,len(allc)-1)]
		
		guildDir = sys.path[0] + f"/logs/guilds/{str(ctx.guild.id)}"
		# selectedLog = open(guildDir + f"/{channel}", "r")
		selectedLog = open(guildDir + f"/{ctx.channel.id}.log", "r")

		userMessages = []
		me = True

		if uname == None: 
			uname = str(ctx.author).split("#")[0]
		else: me = False

		for message in selectedLog.readlines():
			if uname in message: 
				userMessages.append(message)

		if len(userMessages) == 0: 
			await ctx.respond("Couldn't get any quotes. Try again, maybe?")
			return

		msg = userMessages[random.randint(0,len(userMessages)-1)]
		msg = msg.split(maxsplit=2)
		oncesaid = str(msg[2]).split(":", maxsplit=1)[1]

		if me: await ctx.respond(f"*You once said...* {oncesaid}")
		else: await ctx.respond(f"*{uname} once said...* {oncesaid}")