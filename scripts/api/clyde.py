import requests, textwrap
from resources.colour import *


BASE_URL = "https://google-bard1.p.rapidapi.com"

async def doClydeShit(ctx, message):
	await ctx.defer()
	hasResponded = False
	headers = {
		"message": message,
		"userid": "1234",
		"key": "1234",
		"X-RapidAPI-Key": "cb543111a2mshb402f0d41b25d48p11cd7bjsn555d65f484a1",
		"X-RapidAPI-Host": "google-bard1.p.rapidapi.com"
	}

	try:
		response = requests.get(BASE_URL, headers=headers).text

		if len(response) >= 2000:
			for msg in textwrap.wrap(response, 2000):
				try:
					if not hasResponded: await ctx.respond(msg); hasResponded = True
					else: await ctx.channel.send(msg)
				except Exception as err:
					print(RED + str(err) + RESET)
					if not hasResponded: await ctx.respond("I'm currently unable to fufill that request")
					else: await ctx.channel.send("I'm currently unable to fufill that request")
		
		else:
			try:
				if not hasResponded: await ctx.respond(response); hasResponded = True
				else: await ctx.channel.send(response)
			except Exception as err:
				print(RED + str(err) + RESET)
				if not hasResponded: await ctx.respond("I'm currently unable to fufill that request")
				else: await ctx.channel.send("I'm currently unable to fufill that request")

	except Exception as err:
		print(RED + str(err) + RESET)