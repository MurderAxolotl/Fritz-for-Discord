import requests, json, random, string, discord
from craiyon import Craiyon

from concurrent.futures import ThreadPoolExecutor

from scripts.tools.utility import *
from resources.shared import PATH

aeu = string.ascii_uppercase + string.ascii_lowercase

def _randomCode() -> str:
	gs = ""
	
	for i in range(0,7):
		gs = gs + random.choice(aeu)

	return gs

async def generate(ctx, prompt:str):
	await ctx.defer()

	generator = Craiyon()

	try:
		result = await generator.async_generate(prompt)
	
	except Exception as err:
		await ctx.respond(str(err))

	igenc = _randomCode()

	await result.async_save_images(PATH + "/cache/" + igenc)

	allImages = []

	for file in os.listdir(PATH + "/cache/" + igenc):
		allImages.append(discord.File(PATH + "/cache/" + igenc + "/" + file))
	
	await ctx.respond(files=allImages)

	try:
		# Purge the new folder
		os.system("rm -rv " + PATH + "/cache/" + igenc)

	except:
		NotImplemented