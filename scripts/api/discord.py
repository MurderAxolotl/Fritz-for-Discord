"""

THIS MODULE WAS CREATED BY MURDERAXOLOTL
https://github.com/psychon-night

SOURCE: https://github.com/psychon-night/Fritz-for-Discord/blob/main/scripts/api/discord.py

WHEN USED IN YOUR OWN PROJECT, PLEASE PLEASE GIVE CREDIT

COVERED BY THE GPL-3.0 LICENSE: https://github.com/psychon-night/Fritz-for-Discord?tab=GPL-3.0-1-ov-file

"""

import requests, json
from concurrent.futures import ThreadPoolExecutor

from resources.shared import TOKEN, APPLICATIONID
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

### MESSAGE TOOLS ###

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
	
async def get_message(CHANNEL_ID, MESSAGE_ID):
	""" Use the Discord API to get the specified message """

	ENDPOINT = url + "/channels/%s/messages/%s"%(CHANNEL_ID, MESSAGE_ID)

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404

async def trigger_typing(channel):
	""" Trigger typing in `channel` \n\n Returns `0` on success \n\n Returns `-1` or `404` on error"""

	ENDPOINT = url + "/channels/{channel}/typing"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return 0
	except Exception as err:
		print(str(err)); return 404
	
### MEMBER TOOLS ###

### COMMAND TOOLS ###
async def allowInDMs(COMMAND_ID):
	ENDPOINT = url + f"applications/{APPLICATIONID}/commands/{COMMAND_ID}"

	try: 
		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.patch(ENDPOINT, headers=HEADERS, json={"contexts": [0,1,2], "integration_types": [0,1]}))

	except Exception as err:
		print(str(err)); return 404

### GUILD TOOLS ###

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
	

async def get_audit_log(guild):
	""" Get `guild`'s audit log """
	ENDPOINT = url + f"/guilds/{guild}/audit-logs"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404


async def get_guild_members(guild):
	"Get `guild`'s members"
	ENDPOINT = url + f"/guilds/{guild}/members"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404
	
### GUILD BAN TOOLS ###

async def ban_member(guild, user):
	""" Ban `user` from `guild` """
	ENDPOINT = url + f"/guilds/{guild}/bans/{user}"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.put(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		if "Expecting value:" in str(err): return ""
		print(str(err)); return 404


async def unban_member(guild, user):
	""" Unban `user` from `guild` """
	ENDPOINT = url + f"/guilds/{guild}/bans/{user}"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.delete(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404


async def get_bans(guild):
	""" Get `guild`'s bans """
	ENDPOINT = url + f"/guilds/{guild}/bans"

	try: response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: requests.get(ENDPOINT, headers=HEADERS))
	except Exception as err: 
		print(RED + str(err) + RESET)

		return -1
	
	try: return json.loads(response.text)
	except Exception as err:
		print(str(err)); return 404