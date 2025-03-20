"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from concurrent.futures import ThreadPoolExecutor

import asyncio, json, requests

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

	if success == True:
		await ctx.respond(responseJSON["data"]["url"])

	else:
		await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

async def giveRaccFacc(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/fact"))

	responseJSON = json.loads(response.text)
	
	success = responseJSON["success"]

	if success == True:
		await ctx.respond(responseJSON["data"]["fact"])

	else:
		await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

async def giveLynx(ctx):
	await ctx.defer()
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("http://lynx.somnolescent.net/api.php"))

	await ctx.respond(response.text)

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