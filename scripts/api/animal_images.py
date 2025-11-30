"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from concurrent.futures import ThreadPoolExecutor

import asyncio
import json
import requests
import os
import discord

from random import randint

from resources.shared import REGISTERED_DEVELOPERS
from scripts.tools.utility import journal, scramble

loop = asyncio.get_event_loop()

ANIMAL_IMAGE_FAILED_RESPONSE = "Failed to get an image"

async def giveCat(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.thecatapi.com/v1/images/search"))

	await ctx.respond(json.loads(response.text)[0]["url"])

async def giveTrashPanda(ctx, getVideo):
	await ctx.defer()

	if getVideo: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/video?json=true"))
	else:        response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/raccoon?json=true"))

	responseJSON = json.loads(response.text)

	success = responseJSON["success"]

	if success:
		await ctx.respond(responseJSON["data"]["url"])

	else:
		await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

async def giveRaccFacc(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/fact?json=true"))

	responseJSON = json.loads(response.text)

	success = responseJSON["success"]

	if success:
		await ctx.respond(responseJSON["data"]["fact"])

	else:
		await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

async def giveLynx(ctx):
	await ctx.defer()
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.tinyfox.dev/img.json?animal=lynx"))

	await ctx.respond("https://api.tinyfox.dev" + json.loads(response.text)["loc"])

async def giveFox(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/fox"))

	await ctx.respond(json.loads(response.text)["image"])

async def giveWah(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/red_panda"))

	await ctx.respond(json.loads(response.text)["image"])

async def giveWahFact(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/red_panda"))

	await ctx.respond(json.loads(response.text)["fact"])

async def giveDerg(ctx):
	await ctx.defer()

	headers = {
		'User-Agent': 'Fritz-for-Discord/1.0 (github/MurderAxolotl)'
	}

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://e926.net/posts.json?tags=order%3Arandom+score%3A%3E%3D7+limit%3A1+dragon++-female+-overweight+-belly+-duo+-inflatable+-wide_hips+-vore+-hyper+-macro+-diaper+-humanoid+-not_furry+-comic", headers=headers))

	await ctx.respond(json.loads(response.text)["posts"][0]["file"]["url"])
