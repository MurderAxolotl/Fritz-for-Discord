import requests, json
from concurrent.futures import ThreadPoolExecutor

from resources.shared import TOKEN
from resources.colour import *

from scripts.tools.utility import loop

url = "https://discord.com/api/"

HEADERS = {
	"Authorization": "Bot " + TOKEN
}

class parse_tools():
	""" Parsing utility library """

	class messages():
		async def content(messageList):
			""" Returns an iterable list containing message contents """

			messageContents = []

			for messageContext in messageList:
				messageContents.append(messageContext["content"])

			messageContents.reverse()

			return messageContents
		
		async def authors(messageList):
			""" Returns an iterable list containing author names """

			authorContents = []

			for messageContext in messageList:
				authorContents.append(messageContext["author"]["username"])

			authorContents.reverse()

			return authorContents

async def get_channel(ID, key):
	""" Use the Discord API to get channel information """

	ENDPOINT = url + "channels/%s"%ID

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)[key]
	except Exception as err:
		print(str(err)); return 404
	
async def get_guild(ID, key):
	""" Use the Discord API to get guild information """

	ENDPOINT = url + "guilds/%s"%ID

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)[key]
	except Exception as err:
		print(str(err)); return 404

async def query_messages(ID):
	""" Use the Discord API to download the last 50 messages in a channel """

	ENDPOINT = url + "/channels/%s/messages"%ID

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404