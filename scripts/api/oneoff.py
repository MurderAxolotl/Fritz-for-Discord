import requests, asyncio, json, sys, random, discord
from concurrent.futures import ThreadPoolExecutor

from resources.colour import *

from PIL import Image
import base64, base64, os
from io import BytesIO

loop = asyncio.get_event_loop()

async def getRandomJoke(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://official-joke-api.appspot.com/jokes/random"))
	jload = json.loads(response.text)
	setup = jload["setup"]
	punchline = jload["punchline"]

	await ctx.respond("%s %s"%(setup, punchline))

async def giveCat(ctx):
	await ctx.defer()

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.thecatapi.com/v1/images/search"))

	await ctx.respond(json.loads(response.text)[0]["url"])

async def getRandomQuote(ctx):
	keepgoing = 0
	fails = 0

	while keepgoing != 1 and fails < 6:
		try:
			response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.quotable.io/quotes?limit=150&page=%s"%random.randint(1,10)))
			
			quotes = json.loads(response.text)
			await ctx.respond(quotes["results"][random.randint(0,30)]["content"])
			
			return 0

		except Exception as err:
			print(RED + f"Unable to reach quotes API: {str(err)}" + RESET)
			fails += 1

	await ctx.respond("Quote API refused to connect")