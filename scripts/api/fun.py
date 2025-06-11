"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import requests
import asyncio
import discord
import json

import scripts.tools.journal as journal

from resources.shared import QUOTE_WEBHOOK, QUOTE_ID, QUOTE_WEBHOOK_FM, QUOTE_ID_FM, PATH

loop = asyncio.get_event_loop()

# Load quotebook config
with open(f"{PATH}/config/quotebook.json", "r") as qconfig:
	QUOTEBOOK_CONFIG = json.loads(qconfig.read())

guild_list = []

if QUOTEBOOK_CONFIG != "{}":
	for guild in QUOTEBOOK_CONFIG:
		guild_list.append(guild)

async def quotebookMessage(ctx, message:str, author_id:int, author_name:str, aurl:str, force_to_mutts:bool=False):
	await ctx.defer()

	try:
		server = ctx.guild.id

	except: #noqa
		server = 0

	try:
		form = {
			"content": f"{message}",
			"username": f"{author_name}",
			"avatar_url": f"{aurl}"
		}

	except: #noqa
		form = {
			"content": f"{message}",
			"username": f"{author_name}"
		}

	if server == 1362596757862875317 or force_to_mutts:
		request = requests.post(QUOTE_WEBHOOK_FM, json = form)

	elif str(server) in guild_list:
		dynamic_webhook = QUOTEBOOK_CONFIG[str(server)]["channel"]

		request = requests.post(dynamic_webhook, json = form)

	else:
		request = requests.post(QUOTE_WEBHOOK, json = form)

	if request.status_code != "200":
		journal.log(request.text, 4)

	await ctx.respond("Quotebooked", ephemeral=True)

async def forwardToQuotebook(ctx, message:discord.Message, bot:discord.Bot):
	AUTHOR = str(message.author).split("#")[0]

	try:
		server = ctx.guild.id
	except:  #noqa
		server = None

	if server == 1362596757862875317:
		FORWARD_CHANNEL = await bot.fetch_channel(int(QUOTE_ID_FM))

	elif server in guild_list:
		FORWARD_CHANNEL = await bot.fetch_channel(int(QUOTEBOOK_CONFIG[str(server)]["chan_id"]))

	else:
		FORWARD_CHANNEL = await bot.fetch_channel(int(QUOTE_ID))

	await FORWARD_CHANNEL.send(f"{AUTHOR}")
	await message.forward(FORWARD_CHANNEL)

	await ctx.respond("Forwarded to quotebook")
