import g4f, asyncio, textwrap, threading

from concurrent.futures import ThreadPoolExecutor


async def onHeyFritz(ctx, loop):

	sentMessage = await ctx.channel.send("Working....")

	textPrompt = str(ctx.content).split(",", 1)[1]

	try:
		response = await loop.run_in_executor(
			ThreadPoolExecutor(), 
			lambda: g4f.ChatCompletion.create(
			model=g4f.models.gpt_35_turbo, 
			messages=[{"role": "user", "content": textPrompt }], 
		))
	
	except: response = "My LLM failed to respond correctly"

	await sentMessage.delete()
		
	match [len(str(response)) > 0, len(str(response)) > 2000]:
		case [False, _]: await ctx.channel.send("Sorry, it looks like none of my LLMs are responding. Maybe try using the `chatgpt` with `use_legacy` set?")
		case [True, True]:  
			for message in textwrap.wrap(response, 1900): await ctx.channel.send(message)
		case [True, False]: await ctx.channel.send(str(response))