"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import os
import asyncio
import requests
import discord
import random
import string
import sys
import importlib

import scripts.tools.journal as journal

from discord.ext import commands
from resources.colour import *

from resources.shared import PATH, REGISTERED_DEVELOPERS

from discord.ext import commands

loop = asyncio.get_event_loop()

# Peak naming conventions
# I want to fix it, but I don't want to refactor. Next release! (Written on 1.25.0)
async def check(ctx):
	""" Check if the current message instance is a DM. Returns true if this is a DM, false if this is a guild """
	if isinstance(ctx.channel, discord.channel.DMChannel): return True
	else: return False

class bannedFromNSFW(commands.CheckFailure): NotImplemented
class swiperNoSwipingError(commands.CheckFailure): NotImplemented
class bannedUser(commands.CheckFailure): pass
class aprilfools(commands.CheckFailure): pass

### CUSTOM COMMAND CHECK PREDICATES ###

def swiperNoSwiping():
	async def predicate(ctx):
		if not await ctx.bot.is_owner(ctx.author): raise swiperNoSwipingError("Swiper no Swiping")
		return True

	return commands.check(predicate)

def isDeveloper():
	async def predicate(ctx):
		if not str(ctx.author.id) in REGISTERED_DEVELOPERS: raise commands.NotOwner

		return True


	return commands.check(predicate)

def isTheo():
	async def predicate(ctx):
		if not str(ctx.author.id) == "1063584978081951814": raise commands.NotOwner

		return True


	return commands.check(predicate)

def scramble(N=32):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

## Misc utilities ##
# This should not be async. I don't want it to be async. I don't care if it causes blockages.
def loadString(stringFile:str) -> str:
	""" Loads a string from the disk and returns it

	Strings are stored in /resources/strings """

	BASE = PATH + "/resources/strings"

	try:
		file = open(f"{BASE}/{stringFile}.tout", "r")

		contents = file.read()
		file.close()

		return contents

	except FileNotFoundError:
		journal.log(RED + f"ERR: FILE {MAGENTA}{stringFile}{RED} NOT FOUND. RETURNING AN EMPTY STRING TO AVOID CRASH." + RESET, 3)

		return ""

	except Exception as err:
		journal.log(RED + f"ERR: FAILED TO READ {MAGENTA}{stringFile}{RED}: {str(err)}" + RESET, 3)

		return ""
