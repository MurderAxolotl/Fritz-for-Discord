import requests, time, json
from resources.curl_requests import pronouns_page_api
from scripts.tools.utility import *

async def pp_searchTerms(ctx, query):

	# statusMessage = await ctx.send("Searching PronounsPage for \"{que}\"".format(que=query))
	await ctx.defer()

	cookies = pronouns_page_api.terms_cookies
	headers = pronouns_page_api.terms_headers
	response = requests.get('https://en.pronouns.page/api/terms/search/{que}'.format(que=query), cookies=cookies, headers=headers)

	if "term" in response.text:
		await ctx.respond("""Search results for [%s](%s)
%s"""%(query, "<https://en.pronouns.page/dictionary/terminology#%s>"%query, json.loads(response.text)[0]["definition"]))

	else:
		await ctx.respond("No results for \"{que}\". Did you spell it correctly?".format(que=query))

async def pp_searchUser(ctx, query):
	# await deleteMessage(ctx)
	# statusMessage = await ctx.channel.send("Searching users for %s"%query)
	await ctx.defer()

	cookies = pronouns_page_api.terms_cookies
	headers = pronouns_page_api.terms_headers
	response = requests.get('https://en.pronouns.page/api/profile/get/{que}?version=2'.format(que=query), cookies=cookies, headers=headers)

	if "username" in response.text:
		await ctx.respond("Profile located: *[%s](<%s>)*"%(query, "https://en.pronouns.page/@{que2}".format(que2=query)))

	else:
		await ctx.respond("No results for \"%s\". Did you spell it correctly?"%query)