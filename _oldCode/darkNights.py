import random, textwrap
import sys
from time import sleep

import discord


async def getQuote(ctx, count):
	await ctx.defer()
	quotes = ""

	file = open(sys.path[0] + "/resources/res/darknights.txt", "r")
	quoteFile = file.read()
	file.close()
	

	try: file = open(sys.path[0] + "/cache/textdump", "x+")
	except: file = open(sys.path[0] + "/cache/textdump", "w"); file.truncate(0)
	
	quoteList = quoteFile.split("\n")

	gend = 0
	
	while gend != count: 
		quote = quoteList[random.randint(0,len(quoteList)-1)]
		quotes = quotes + quote + "\n"
		gend += 1

	file.write(quotes); file.close()
	
	if count > 1: await ctx.reply(file=discord.File(sys.path[0] + "/cache/textdump", "darkNights.txt"))
	else: await ctx.reply(quote)