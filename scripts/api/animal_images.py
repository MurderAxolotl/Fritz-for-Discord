from concurrent.futures import ThreadPoolExecutor

import asyncio, json, requests

loop = asyncio.get_event_loop()

async def giveCat(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.thecatapi.com/v1/images/search"))

	await ctx.respond(json.loads(response.text)[0]["url"])

async def giveTrashPanda(ctx):
	await ctx.defer()

	# response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/raccoon"))
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://serpapi.com/search.json?q=raccoon&engine=google_images&ijn=0"))

	await ctx.respond(json.loads(response.text)["image"])

async def giveLynx(ctx):
	await ctx.defer()
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("http://lynx.somnolescent.net/api.php"))

	await ctx.respond(response.text)

async def giveFox(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://some-random-api.com/animal/fox"))

	await ctx.respond(json.loads(response.text)["image"])
