import scripts.api.discord as discord_fancy, requests, json, asyncio

from scripts.tools.utility import loop
from resources.colour import *
from resources.shared import TOKEN, APPLICATIONID
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
	"Authorization": "Bot " + TOKEN
}


async def hook():
	ENDPOINT = f"https://discord.com/api/applications/{APPLICATIONID}/commands"

	try: 
		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))

	except Exception as err:
		print(RED + "Failed to configure commands through API: %s"%str(err) + RESET)

		return -1
	
	try:
		jtext = json.loads(response.text)
		for COMMAND_NAME in jtext:
			await asyncio.sleep(1)
			print(YELLOW + "[COMMAND MIXIN] Processing for " + COMMAND_NAME["id"] + RESET)
			try: await discord_fancy.allowInDMs(COMMAND_NAME["id"])
			except Exception as err: print(RED + str(err) + RESET)

	except Exception as err:
		print(RED + str(err) + RESET)