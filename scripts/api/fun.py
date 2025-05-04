"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import requests
import asyncio
import json
import sys
import random
import urllib
import os
import discord

from types import NoneType

from resources.colour import *
from resources.shared import QUOTE_WEBHOOK, QUOTE_ID, journal, QUOTE_WEBHOOK_FM, QUOTE_ID_FM

loop = asyncio.get_event_loop()

async def quotebookMessage(ctx, message:str, author_id:str, author_name:str, aurl:str):
	await ctx.defer()

	try:
		server = ctx.guild.id
	except: server = None

	try:
		form = {
			"content": f"{message}",
			"username": f"{author_name}",
			"avatar_url": f"{aurl}"
		}
	except:		
		form = {
			"content": f"{message}",
			"username": f"{author_name}"
		}

	if server != 1362596757862875317:
		request = requests.post(QUOTE_WEBHOOK, json = form)
	else:
		request = requests.post(QUOTE_WEBHOOK_FM, json = form)

	if request.status_code != "200":
		journal.log(request.text, 4)

	await ctx.respond("Quotebooked", ephemeral=True)

async def forwardToQuotebook(ctx, message:discord.Message, bot:discord.Bot):
	AUTHOR = str(message.author).split("#")[0]

	try:
		server = ctx.guild.id
	except: server = None

	if server != 1362596757862875317: FORWARD_CHANNEL = await bot.fetch_channel(QUOTE_ID)
	else: FORWARD_CHANNEL = await bot.fetch_channel(QUOTE_ID_FM)

	await FORWARD_CHANNEL.send(f"{AUTHOR}")
	await message.forward(FORWARD_CHANNEL)

	await ctx.respond("Added to quotebook")