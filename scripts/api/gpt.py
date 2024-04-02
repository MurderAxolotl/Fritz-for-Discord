from discord import Guild
import textwrap, g4f
from concurrent.futures import ThreadPoolExecutor

from scripts.tools.utility import *

from types import NoneType

from resources.shared import AI_BLACKLIST

LEGACY_MODES = ["none", "turbo", "davinci", "fast"]

async def generateResponse(ctx, inPrompt, loop, legacy_mode = "none"):

	match not isinstance(ctx.guild, NoneType):
		case True:
			match ctx.guild.id in AI_BLACKLIST:
				case True: await ctx.respond("That command is disabled on this server"); return -1

	if   legacy_mode == "none"   : MODEL = g4f.models.gpt_4
	elif legacy_mode == "turbo"  : MODEL = g4f.models.gpt_35_turbo
	elif legacy_mode == "fast"   : MODEL = g4f.models.gpt_35_long

	await ctx.defer()

	await asyncio.sleep(1)
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: g4f.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": inPrompt }], ))

	sent = 0

	if len(str(response)) > 0: 
		if len(str(response)) > 1920:
			for msg in textwrap.wrap(response, 1920, drop_whitespace=False, replace_whitespace=False):
				try: 
					if len(msg) != 0: 
						if sent == 0: await ctx.respond(msg)
						else: await ctx.channel.send(msg)
					else: print(RED + "WARN: Dropping empty message. Probably white-space?" + RESET)
				except: await ctx.channel.send(msg)
				sent += 1

		else: await ctx.respond(response)

	else: await ctx.respond("Sorry, it looks like none of my LLMs are responding. Maybe try setting `use_legacy`?", ephemeral=True)