""" Provides on-message features, such as the `Hey Fritz` prompt """

"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import g4f, asyncio, textwrap, sys, requests, json, random
from concurrent.futures import ThreadPoolExecutor

from resources.colour import *


async def onHeyFritz(ctx, loop):

	sentMessage = await ctx.channel.send("Working....")

	textPrompt = str(ctx.content).split(",", 1)[1]

	try:
		response = await loop.run_in_executor(
			ThreadPoolExecutor(),
			lambda: g4f.ChatCompletion.create(model=g4f.models.gpt_4, messages=[{"role": "user", "content": textPrompt }], )
		)
	
	except Exception as err: 
		response = "My LLM failed to respond correctly"
		print(RED + "LLM ERR: " + str(err) + RESET)

	await sentMessage.delete()
		
	match [len(str(response)) > 0, len(str(response)) > 2000]:
		case [False, _]: await ctx.channel.send("Sorry, it looks like none of my LLMs are responding. Maybe try using the `chatgpt` with `use_legacy` set?")
		case [True, True]:  
			for message in textwrap.wrap(response, 1900): await ctx.channel.send(message)
		case [True, False]: await ctx.channel.send(str(response))

async def lyricLoader(ctx):
	# print(sys.path[0] + "/resources/docs/lyrics/%s"%str(ctx.content))
	# print(str(ctx.content), ": ", str(ctx.content).lower() in os.listdir(sys.path[0] + "/resources/docs/lyrics/"))

	lyric_target = sys.path[0] + "/resources/docs/lyrics/" + str(ctx.content).lower()

	if (lyric_target == sys.path[0] + "/resources/docs/lyrics/"): return -1

	try:
		for line in open(lyric_target, "r").read().splitlines():
			
			if len(line) != 0:
				try: await ctx.channel.send(line, silent=True)
				except: NotImplemented # Skip the line, it's probably not valid

			await asyncio.sleep(1)
	
	except: NotImplemented # Fail silently, too lazy