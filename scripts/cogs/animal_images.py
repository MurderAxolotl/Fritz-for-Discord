"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from concurrent.futures import ThreadPoolExecutor

import asyncio
import json
import requests
import discord
from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES

ANIMAL_IMAGE_FAILED_RESPONSE = "Failed to get an image"

class AnimalImageView(discord.ui.DesignerView):
	def __init__(self, image_url="", *, spoiler:bool=False):
		super().__init__(timeout=None)

		media_gallery = discord.ui.MediaGallery()

		gallery_image = discord.MediaGalleryItem(image_url, spoiler=spoiler)
		media_gallery.append_item(gallery_image)

		super().add_item(media_gallery)

class AnimalImages(commands.Cog):
	loop = asyncio.get_event_loop()

	def __init__(self, bot):
		self.bot = bot

	# CAT PICTURE #
	@commands.slash_command(name="givecat", description="Get a random cat photo", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def givecat(self, ctx):
		await ctx.defer()

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.thecatapi.com/v1/images/search"))
		image_url = json.loads(response.text)[0]["url"]

		await ctx.respond(view=AnimalImageView(image_url=image_url))

	# LYNX PICTURE #
	@commands.slash_command(name="givelynx", description="Get a random lynx photo", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def givelynx(self, ctx):
		await ctx.defer()
		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.tinyfox.dev/img.json?animal=lynx"))
		image_url = "https://api.tinyfox.dev" + json.loads(response.text)["loc"]

		await ctx.respond(view=AnimalImageView(image_url=image_url))

	# FOX PICTURE #
	@commands.slash_command(name="givefox", description="Get a random fox photo", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def givefox(self, ctx):
		await ctx.defer()

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/fox"))
		image_url = json.loads(response.text)["image"]

		await ctx.respond(view=AnimalImageView(image_url=image_url))

	# RACOON PICTURE #
	@commands.slash_command(name="giveracc", description="Get a random raccoon photo (or video)", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def trashpanda(self, ctx, *, video:bool=False):
		await ctx.defer()

		if video:
			response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/video?json=true"))
		else:
			response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/v1/raccoon?json=true"))

		responseJSON = json.loads(response.text)
		image_url = responseJSON["data"]["url"]

		success = responseJSON["success"]

		if success:
			await ctx.respond(view=AnimalImageView(image_url=image_url))

		else:
			await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

	# WAH IMAGE #
	@commands.slash_command(name="givewah", description="Get a random red panda photo", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def wahimage(self, ctx):
		await ctx.defer()

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/red_panda"))
		image_url = json.loads(response.text)["image"]

		await ctx.respond(view=AnimalImageView(image_url=image_url))

	# DRAGON PICTURE #
	@commands.slash_command(name="givederg", description="Get a random dragon photo", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def givederg(self, ctx):
		await ctx.defer()

		headers = {
			'User-Agent': 'Fritz-for-Discord/1.0 (github/MurderAxolotl)'
		}

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://e926.net/posts.json?tags=order%3Arandom+score%3A%3E%3D7+limit%3A1+dragon++-female+-overweight+-belly+-duo+-inflatable+-wide_hips+-vore+-hyper+-macro+-diaper+-humanoid+-not_furry+-comic", headers=headers))
		image_url = json.loads(response.text)["posts"][0]["file"]["url"]

		await ctx.respond(view=AnimalImageView(image_url=image_url))

	# RACOON FACT #
	@commands.slash_command(name="raccfacc", description="Get a random raccoon fact", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def raccfacc(self, ctx):
		await ctx.defer()

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.racc.lol/fact?json=true"))

		responseJSON = json.loads(response.text)

		success = responseJSON["success"]

		if success:
			await ctx.respond(responseJSON["data"]["fact"])

		else:
			await ctx.respond(ANIMAL_IMAGE_FAILED_RESPONSE)

	# WAH FACT #
	@commands.slash_command(name="wahfact", description="Get a random red panda fact", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def wahfact(self, ctx):
		await ctx.defer()

		response = await self.loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/red_panda"))

		await ctx.respond(json.loads(response.text)["fact"])
