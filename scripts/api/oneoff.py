import requests, asyncio, json, sys, random, discord
from concurrent.futures import ThreadPoolExecutor

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