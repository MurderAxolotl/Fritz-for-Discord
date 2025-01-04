from private.tok import SD_TOK
import json, asyncio, os, random, requests, json, base64
from PIL import Image
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor

from scripts.tools.utility import *

async def doGen(ctx, prompt, count):
	loops = 0
	originalPromptMessage = None

	while loops != count:

		loop = asyncio.get_event_loop()
		if loops == 0: await ctx.defer()

		log = open(sys.path[0] + "/logs/prompt.log ", "a")
		log.write(str(ctx.author) + ": " + prompt + "\n")
		log.close()

		url = "https://api.wizmodel.com/sdapi/v1/txt2img"

		payload = json.dumps({
		"prompt": prompt,
		"steps": 50
		})
		headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer %s'%SD_TOK
		}


		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.request("POST", url, headers=headers, data=payload))

		base64_string = response.json()['images'][0]
		image_data = base64.b64decode(base64_string)
		image_bytes = BytesIO(image_data)

		indexID = len(os.listdir(sys.path[0] + "/cache/"))

		id = random.randint(0,25555)

		cacheDir = sys.path[0] + "/cache"
		file = cacheDir + "/temp_%s-%s.png"%(id, indexID)

		image = Image.open(image_bytes)
		image.save(file)

		with open(file, "rb") as outFile:
			if loops == 0: originalPromptMessage = await ctx.respond(file=discord.File(outFile, "generated_%s-%s.png"%(id, indexID)))
			else: 
				await ctx.channel.send(prompt, file=discord.File(outFile, "generated_%s-%s.png"%(id, indexID)))

		loops += 1