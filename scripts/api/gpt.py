import textwrap, g4f
from concurrent.futures import ThreadPoolExecutor
from scripts.tools.utility import *

from types import NoneType

from resources.shared import AI_BLACKLIST

LEGACY_MODES = ["none", "turbo", "davinci"]

async def generateResponse(ctx, inPrompt, loop, legacy_mode = "none"):

	match not isinstance(ctx.guild, NoneType):
		case True:
			match ctx.guild.id in AI_BLACKLIST:
				case True: await ctx.respond("That command is disabled on this server"); return -1

	if   legacy_mode == "none"   : MODEL = g4f.models.gpt_35_long
	elif legacy_mode == "turbo"  : MODEL = g4f.models.gpt_35_turbo
	elif legacy_mode == "davinci": MODEL = g4f.models.text_davinci_003

	await ctx.respond("Working...", ephemeral=True)

	with ctx.typing():
		await asyncio.sleep(1)
		response = await loop.run_in_executor(ThreadPoolExecutor(), lambda: g4f.ChatCompletion.create(model=MODEL, messages=[{"role": "user", "content": inPrompt }], ))

		author = str(ctx.author).split("#0")[0]

		if len(str(response)) > 0: 
			if len(str(response)) > 1024:
				numEmbeds = 0

				embed = discord.Embed(
					title="", 
					description="%s requested: %s"%(author, inPrompt), 
					colour=discord.Colour.dark_purple(),
				)

				for msg in textwrap.wrap(response, 1024):
					if numEmbeds != 9: 
						embed.add_field(name="", value=msg, inline=False)
						numEmbeds += 1

					else: 
						embed = discord.Embed(
							title="", 
							description="%s requested: %s"%(author, inPrompt), 
							colour=discord.Colour.dark_purple(),
						)
						
						embed.add_field(name="", value=msg, inline=False)
						numEmbeds = 1
						
						await ctx.channel.send(embed=embed)

				await ctx.channel.send(embed=embed)

			else: 
				embed = discord.Embed(
					title="",
					description="%s requested: %s"%(author, inPrompt),
					colour=discord.Colour.dark_purple(),
				)

				embed.add_field(name="", value=response, inline=False)
				
				await ctx.channel.send(embed=embed)

		else: 
			await ctx.respond("Sorry, it looks like none of my LLMs are responding. Maybe try setting `use_legacy`?", ephemeral=True)