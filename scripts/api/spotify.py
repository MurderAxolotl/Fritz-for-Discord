import json
import requests

from urllib.parse import quote

from scripts.tools.utility import *
from resources.shared import *

async def searchSpotify(ctx, query, count):

	if count < 0 or count > 50:
		await ctx.channel.send("Invalid result limit; defaulting to 10")
		count = 10

	ssearch_params = {'q': "'" + query + "'", 'type': 'track', 'limit': '%s'%count, 'offset': '0'}

	data = {'grant_type': 'client_credentials','client_id': '709308bdbeb94c68bfd4cb456a47fa15', 'client_secret': '2c8081761467492c8fc602c504268909'}

	auth_token = json.loads(requests.post('https://accounts.spotify.com/api/token', data=data).text)["access_token"]

	response = requests.get('https://api.spotify.com/v1/search', params=ssearch_params, headers={'Authorization': 'Bearer %s'%auth_token})

	# await infoMessage.edit("Parsing response...")
	await ctx.defer()

	res = json.loads(response.text)

	if "tracks" in res: songList = res["tracks"]["items"]
	else: await ctx.respond("EEK! API sent a garbage response, I can't read this!"); return

	totalCombined = """"""

	totalLen = 0

	for track in songList:
		title = track["name"]
		artist = track["artists"][0]["name"]	
		isExplicit = track["explicit"]
		trackPreview = track["external_urls"]["spotify"]

		combined = """[%s - %s](<%s>) %s"""%(title, artist, trackPreview, "ᴱ" if isExplicit == True else "")

		totalLen += len(combined)

		totalCombined = totalCombined + """
""" + combined
		
		if totalLen > 1500:
			# await infoMessage.edit("Showing search results for %s"%query)
			await ctx.respond(totalCombined)
			totalCombined = """"""
			totalLen = 0
	
	# print(res)

	if len(songList) > 0:
		# await infoMessage.edit("Showing search results for %s"%query)
		await ctx.respond(totalCombined)

	else:
		await ctx.respond("Search returned no results for %s"%query)