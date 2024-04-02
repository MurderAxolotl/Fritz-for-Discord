import requests, json, sys
import requests, asyncio
from urllib import parse

from io import BytesIO

from PIL import Image
from pyzbar.pyzbar import decode


from concurrent.futures import ThreadPoolExecutor

loop = asyncio.get_event_loop()
url = "https://api.qrcode-monkey.com//qr/custom"

headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "cb543111a2mshb402f0d41b25d48p11cd7bjsn555d65f484a1",
	"X-RapidAPI-Host": "qrcode-monkey.p.rapidapi.com"
}

design_stylized = {
		"config": {
			"bgColor": "#FFFFFF", "body": "japnese", "bodyColor": "#3400E0", "brf1": [], "brf2": [], "brf3": [], "erf1": [], "erf2": [], "erf3": [], "eye": "frame13", "eye1Color": "#8000FF", "eye2Color": "#8000FF", "eye3Color": "#8000FF", "eyeBall": "ball15", "eyeBall1Color": "#C300FF", "eyeBall2Color": "#C300FF", "eyeBall3Color": "#C300FF", "gradientColor1": "", "gradientColor2": "", "gradientOnEyes": 'false', "gradientType": "linear", "logo": "", "logoMode": "default"
		},
		"size": 300,
		"download": True,
		"file": "png"
	}

design_compatibility = {
		"config": {"bgColor": "#FFFFFF", "body": "square", "bodyColor": "#000000", "brf1": [], "brf2": [], "brf3": [], "erf1": [], "erf2": [], "erf3": [], "eye": "frame0", "eye1Color": "#000000", "eye2Color": "#000000", "eye3Color": "#000000", "eyeBall": "ball0", "eyeBall1Color": "#000000", "eyeBall2Color": "#000000", "eyeBall3Color": "#000000", "gradientColor1": "", "gradientColor2": "", "gradientOnEyes": 'true', "gradientType": "linear", "logo": "", "logoMode": "default"
		},
		"size": 300,
		"download": True,
		"file": "png"
	}

designTypes = {'compatible':design_compatibility, 'stylized (default)':design_stylized, 'max ECC':'max ECC'}

async def read_cv(ctx, qr_image):
	await ctx.defer()

	response = requests.get(qr_image)
	img = Image.open(BytesIO(response.content))

	qrs = decode(img)

	if len(qrs) != 0: 
		try: await ctx.respond("QR SCANNED. Data: " + str(qrs[0].data.decode()))
		except: 
			try: await ctx.channel.send("QR SCANNED. Data: " +  str(qrs[0].data.decode()))
			except: await ctx.channel.send("QR data was scanned, but it cannot be sent. Does the QR's data exceed 2000 chars?")
	else: await ctx.respond("Couldn't detect any QR codes or barcodes")

async def read(ctx, qr_image_url):
	await ctx.defer()
	parsed = parse.quote(qr_image_url)
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.post("http://api.qrserver.com/v1/read-qr-code/?fileurl=%s"%parsed))

	try: await ctx.respond("Scanned QRC! <" + json.loads(response.text)[0]["symbol"][0]["data"] + ">")
	except Exception as err: await ctx.respond("Unable to parse QR code. Is it valid?")

async def createQR(ctx, qrData, designType):
	await ctx.defer()
	# print(designType)

	if designType != 'max ECC':

		payload = designTypes[designType]
		payload["data"] = qrData

		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.post(url, json=payload, headers=headers))
		
		if "imageUrl" in response.text:
			await ctx.respond("https:" + str(json.loads(response.text)["imageUrl"]))
		else:
			await ctx.respond("API failed to return the QR code")

	else: await maxECC(ctx, qrData)

async def maxECC(ctx, qrData):
	url = "http://api.qrserver.com/v1/create-qr-code/?data=%s&ecc=H"%parse.quote(qrData)

	await ctx.respond(url)