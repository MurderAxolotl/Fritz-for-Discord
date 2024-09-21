### WARNING: THIS IS BUILT EXPLICITY FOR MY INSTANCE OF FRITZ. DO NOT ATTEMPT TO USE IT, IT WILL BREAK STUFF ###
# Pulls from https://docs.google.com/spreadsheets/d/1isjPlXMykGGruSFUgMJL1V6SumL3CC3ibIuCCyLA9us/edit?gid=2021885162#gid=2021885162
# Only works with one-response cards rn, I don't feel like fuckin' with two

import os, sys, time
import language_tool_python as langTool

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from resources.shared import *

# Configuration to make Google happy
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHE_ID = "1isjPlXMykGGruSFUgMJL1V6SumL3CC3ibIuCCyLA9us"

SEARCH_RANGE = "MCL!A3:D5987" # I only care about Main!A3:A5987 and Main!D3:D5987, but I'd rather not make multiple calls
#SEARCH_RANGE = "Main!A3:D500" # Smaller group for testing. I'd rather not cook my dev machine

# Configuration to make me happy
CREDS_PATH = sys.path[0] + "/private/googleCreds.json"
TOKEN_PATH = sys.path[0] + "/private/googleToken.json"

async def get_auth():
	""" Authenticates the user and return valid credentials """
	credential = None

	if os.path.exists(TOKEN_PATH): credential = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

	if not credential or not credential.valid:
		if credential and credential.expired and credential.refresh_token: credential.refresh(Request())

		else:
			print(f"login flow :3 {CREDS_PATH=}")
			login_flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)

			credential = login_flow.run_local_server(port=0)
			
			with open(TOKEN_PATH, "w") as token:
				token.write(credential.to_json())

	return credential

def find_instance(data, instance_id):
	""" Finds the instance of instance_id in data, presumably """

	for row in data:
		# What the FUCK am I doing
		if str(instance_id) in str(row): return list(row)

	return "notFound"

async def read_sheet(ctx, prompt_id, response_id):
	""" Reaches out and does the delicious scraping. Call this """	

	await ctx.defer()

	auth = await get_auth()
	formatter = langTool.LanguageTool("en-US")

	try:
		service = build("sheets", "v4", credentials=auth)

		sheet = service.spreadsheets()
		result = (
			sheet.values().get(spreadsheetId=SHE_ID, range=SEARCH_RANGE).execute()
		)

		values = result.get("values", [])

		if not values:
			print("Who did this?!?! >  " + values)
			await ctx.respond("API didn't return valid data")
			return ":("
		
		# time it :(
		start_time = time.time()
		prompt = find_instance(values, prompt_id  )
		respon = find_instance(values, response_id)
		print("------- END! -------")
		print("Took %s"%(time.time() - start_time))

		if prompt != "notFound": prompt_text:str = prompt[3]
		else: await ctx.respond(f"Couldn't find index {prompt_id}"); return

		if respon != "notFound": respon_text:str = respon[3]
		else: await ctx.respond(f"Couldn't find index {response_id}"); return

		if "_" in prompt_text:
			index = prompt_text.index("_")
			
			partial = prompt_text[:index] + respon_text + prompt_text[index:]
			final_prompt_text = partial.replace("_", "").replace(".", "").lower()
			await ctx.respond(formatter.correct(final_prompt_text))

		else:
			await ctx.respond(f"{prompt_text} {respon_text}")
		
	except Exception as err: print("Why are you like this :( > " + str(err))

	formatter.close()