import json, asyncio
import random
import requests

from concurrent.futures import ThreadPoolExecutor

from scripts.tools.utility import *

loop = asyncio.get_event_loop()
modeKeys = {"realistic":84, "dark_fantasy":121, "horror":123, "anime":117, "sci-fi":109, "malev":40, "lines":47, "spectral":63, "hdr":52}
nsfw_modeKeys = {"furry1":"yiffymix_v34", "furry2":"furry", "hyperrealism":"realisticVisionV51_v51VAE", "homoerotic":"model6", "realism":"model8", "cartoon3d":"realcartoon3d_v8", "hentai":"hassakuHentaiModel_v13", "rev":"revAnimated_v122EOL", "pixelart":"dreamshaperPixelart_v10", "hd_female":"buxomBritsV12_v10", "hd_male":"virileReality_v30BETA2", "artUniverse":"artUniverse_v80", "mj_cracked":"model9", "hd_realism":"model7", "deliberate":"model3"}

BASE_URL = "https://paint.api.wombo.ai/api/v2/tasks/"

class blocking():
	def b1(): return requests.post("https://securetoken.googleapis.com/v1/token?key=", data={"grant_type":"refresh_token", "refresh_token":""}).text

def threadedPost(kwargs):
	requests.post(**kwargs)

async def generateFromPrompt(ctx, prompt, mode='realistic'):

	log = open(sys.path[0] + "/logs/prompt.log ", "a")
	log.write(str(ctx.author) + ": " + prompt + "\n")
	log.close()

	# await deleteMessage(ctx)

	if (mode == "help" or prompt == "help"): 
		strText = ""

		for style in modeKeys.keys():
			if len(strText)!=0:strText = strText + ", *%s*"%style
			else:strText = strText + "*%s*"%style

	if (mode in modeKeys.keys()):modeID = modeKeys[mode]
	else: modeID = modeKeys['realistic']

	requestID = ""

	await ctx.defer()

	token = json.loads(await loop.run_in_executor(ThreadPoolExecutor(), blocking.b1))

	headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://dream.ai/',
    'x-app-version': 'WEB-2.0.0',
    'Authorization': 'bearer %s'%token["access_token"],
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://dream.ai',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

	data = '{"is_premium":false,"input_spec":{"prompt":"%s","style":%s,"display_freq":10}}'%(prompt, modeID)

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.post('https://paint.api.wombo.ai/api/v2/tasks/', headers=headers, data=data))
	# print(response.text)

	if ("pending" in response.text):
		requestID = json.loads(response.text)["id"]
		await asyncio.sleep(1)

	elif ("\"is_nsfw\":true" in response.text):
		# await ctx.respond("NSFW is a premium feature, and I am NOT paying so you can get some AI-generated porn. Here's a few porn sites instead: [PornHub](<https://pornhub.com) [e621](<https://e621.net>) [xhamster](<https://xhamster.com>)")
		# await ctx.respond("NSFW is a premium feature provided by the backend. Switching to NSFW API...")
		
		await nsfwGenerate(ctx, prompt, "hd_realism")

	else: 
		await ctx.respond("API did not return an image"); return
		# await ctx.respond(response.text); return

	apiResponse = ""
	timeSpent = 0

	while not ("completed" in apiResponse) or timeSpent < 60:
		apiResponse = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get('https://paint.api.wombo.ai/api/v2/tasks/%s'%requestID, headers=headers, data=data).text)

		if not ("completed" in apiResponse): await asyncio.sleep(2)

		timeSpent += 2

	if ("completed" in apiResponse):
		photoURL = json.loads(apiResponse)["photo_url_list"][0]
		await ctx.respond(photoURL)
		# print(response.text)
		

	else: await ctx.respond("API timed out")

async def nsfwGenerate(ctx, prompt, mode):
	try:await ctx.defer()
	except:NotImplemented

	log = open(sys.path[0] + "/logs/prompt.log ", "a")
	log.write(str(ctx.author) + ": " + prompt + "\n")
	log.close()

	strText = ""
	for style in nsfw_modeKeys.keys():
		if len(strText)!=0:strText = strText + ", *%s*"%style
		else:strText = strText + "*%s*"%style

	if (mode in nsfw_modeKeys.keys()):modeID = nsfw_modeKeys[mode]
	else: modeID = nsfw_modeKeys['hd_realism']

	headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://sexy.ai',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
	}

	data = '{"modelName":"%s","prompt":"HD %s","negprompt":"","restoreFaces":true,"sessionID":"1b8b73ec-c61e-49e5-b6e3-7142d4c21a73","steps":20,"width":512,"height":640,"folderID":"","seed":%s,"subseed":null,"subseed_strength":0.1,"sampler":"DPM++ 2M Karras","cfgscale":7}'%(modeID, prompt, random.randint(1000000000000000, 9999999999999999))
	# print(data)
	
	await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.sexy.ai/getSelfUser?sessionID=1b8b73ec-c61e-49e5-b6e3-7142d4c21a73&isAtLeast18Confirmed=true", headers=headers))

	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.post('https://api.sexy.ai/generateImage', headers=headers, data=data))

	if not json.loads(response.text)["hasError"]:
		genID = json.loads(response.text)["payload"]["imageID"]

		# print(genID)
	
	else: 
		await ctx.respond("API did a fucky wucky"); print(response.text)
		return

	keepGen = True
	while keepGen:
		await asyncio.sleep(2)
		print("https://api.sexy.ai/getItemStatus?imageID=%s&sessionID=1b8b73ec-c61e-49e5-b6e3-7142d4c21a73"%genID)
		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get("https://api.sexy.ai/getItemStatus?imageID=%s&sessionID=1b8b73ec-c61e-49e5-b6e3-7142d4c21a73"%genID, headers=headers))

		# print(response.text)

		if json.loads(response.text)["payload"]["status"] == "complete":
			keepGen = False

	imageURL = json.loads(response.text)["payload"]["url"]
	print(imageURL)

	await ctx.respond(imageURL)