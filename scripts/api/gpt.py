import asyncio
import sys, requests, textwrap
import g4f, re

from concurrent.futures import ThreadPoolExecutor

# from g4f.Provider import AItianhu, Aichat, Bard, Bing, ChatBase, ChatgptAi, OpenaiChat, Vercel, You, Yqcloud

from scripts.tools.utility import *

async def generateResponse(ctx, inPrompt, loop, model='text-davinci-003'):
	allowed_models = ['code-davinci-002', 'text-ada-001', 'text-babbage-001', 'text-curie-001', 'text-davinci-002', 'text-davinci-003', 'palm', 'gpt-4-0613']

	await ctx.defer()
	
	# response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: g4f.Completion.create(model=model, prompt=inPrompt))
	response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: g4f.ChatCompletion.create(model=g4f.models.gpt_35_long, messages=[{"role": "user", "content": inPrompt }], ))

	if len(str(response)) > 0: 
		if len(str(response))>1800:
			numEmbeds = 0
			embed = discord.Embed(title="", description="%s requested: %s"%(str(ctx.author), inPrompt), colour=discord.Colour.dark_purple(),)

			for msg in textwrap.wrap(response, 1800):
				if numEmbeds != 9: embed.add_field(name="", value=msg, inline=False); numEmbeds += 1
				else: embed = discord.Embed(title="", description="%s requested: %s"%(str(ctx.author), inPrompt), colour=discord.Colour.dark_purple(),); embed.add_field(name="", value=msg, inline=False); numEmbeds = 1; await ctx.respond(embed=embed)

			await ctx.respond(embed=embed)

		else: 
			embed = discord.Embed(
				title="",
				description="%s requested: %s"%(str(ctx.author), inPrompt),
				colour=discord.Colour.dark_purple(),
			)
			
			await ctx.respond(embed=embed)
	else: await ctx.respond("Language backend is not responding")