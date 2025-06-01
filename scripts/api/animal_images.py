"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from concurrent.futures import ThreadPoolExecutor

import asyncio, json, requests, os, discord

from random import randint

from resources.shared import SNEP_FOLDER
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

async def giveSnep(ctx):
	await ctx.defer()

	# I can't find a good snow leopard image API, so these are stored locally
	# This isn't a great solution, but... I don't want to keep them in Fritz's
	# directory either... so, fixed-path it is :3

	if SNEP_FOLDER == None:
		journal.log("No snep folder configured, refusing request")
		await ctx.respond("No sneps are available at this time")

	else:
		AVAILABLE_SNEPS = os.listdir(SNEP_FOLDER)

		if len(AVAILABLE_SNEPS) == 0:
			journal.log("No snep folder configured, refusing request")
			await ctx.respond("No sneps are available at this time")

		else:
			selectedSnep = AVAILABLE_SNEPS[randint(0,len(AVAILABLE_SNEPS)-1)]

			snep_path = f"{SNEP_FOLDER}/{selectedSnep}"
			
			try: filetype = selectedSnep.split(".")[1]
			except:
				# Well fuck. Assume jpeg, most of them should be jpeg images anyways
				filetype = "jpeg"

			await ctx.respond(file=discord.File(snep_path, scramble(16) + f".{filetype}"))