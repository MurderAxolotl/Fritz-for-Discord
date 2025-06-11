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

from resources.shared import SNEP_FOLDER, REGISTERED_DEVELOPERS
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

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/fact"))

	responseJSON = json.loads(response.text)

	success = responseJSON["success"]

	if success:
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

async def giveSnep(ctx, dirInfo:bool=False, excludeVideos:bool=False):
	await ctx.defer()

	# I can't find a good snow leopard image API, so these are stored locally
	# This isn't a great solution, but... I don't want to keep them in Fritz's
	# directory either... so, fixed-path it is :3
	# Past me, what the *fuck* were you doing?

	if SNEP_FOLDER is None:
		journal.log("No snep folder configured, refusing request")
		await ctx.respond("No sneps are available at this time")

	elif not dirInfo:
		AVAILABLE_SNEPS = os.listdir(SNEP_FOLDER)

		if len(AVAILABLE_SNEPS) == 0:
			journal.log("No snep folder configured, refusing request")
			await ctx.respond("No sneps are available at this time")

		else:
			selectedSnep = AVAILABLE_SNEPS[randint(0,len(AVAILABLE_SNEPS)-1)]

			snep_path = f"{SNEP_FOLDER}/{selectedSnep}"

			try:
				filetype = selectedSnep.split(".")[1]
			except:
				# Well fuck. Assume jpeg, most of them should be jpeg images anyways
				# Of note, this will break images twt
				filetype = "jpeg"

			await ctx.respond(file=discord.File(snep_path, scramble(16) + f".{filetype}"))

	else:
		AVAILABLE_SNEPS = os.listdir(SNEP_FOLDER)

		await ctx.respond(f"There are {len(AVAILABLE_SNEPS)} snep files available")

async def add_file_to_snep_folder(ctx: discord.ApplicationContext, message:discord.Message|None=None):
	await ctx.defer()

	successful = 0
	failed     = 0

	adder_id = ctx.user.id #pyright:ignore
	attachments:list[discord.Attachment] = message.attachments #pyright:ignore

	if len(attachments) == 0:
		await ctx.respond("No attachments detected in this message. Hyperlinked images are not supported")
		return

	if str(adder_id) not in REGISTERED_DEVELOPERS:
		await ctx.respond("Only a developer may use this feature")
		return

	# Now we can actually extract the images
	failedBecauseExists = False
	for file in attachments:
		print(file.filename, file.size, file.url)

		response = requests.get(file.url)

		try:
			# Check if the file already exists. Fail if it does
			if file.filename in os.listdir(f"{SNEP_FOLDER}"):
				failed += 1
				failedBecauseExists = True

			else:
				with open(f"{SNEP_FOLDER}/{file.filename}", "wb") as file:
					file.write(response.content)

				successful += 1

		except FileExistsError:
			failedBecauseExists = True
			failed += 1

	feedback = f"{successful} file(s) added to folder" if not failedBecauseExists else f"{successful} file(s) added to folder, {failed} file(s) already in folder"

	await ctx.respond(feedback)
