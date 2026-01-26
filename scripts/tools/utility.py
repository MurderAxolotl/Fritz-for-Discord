"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import os
import asyncio
import discord
import random
import string

import scripts.tools.journal as journal

from discord.ext import commands
from resources.colour import MAGENTA, SEAFOAM

from resources.shared import RESOURCE_PATH, REGISTERED_DEVELOPERS, CACHE_PATH

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

	BASE = RESOURCE_PATH + "/strings"

	try:
		file = open(f"{BASE}/{stringFile}.tout", "r")

		contents = file.read()
		file.close()

		return contents

	except FileNotFoundError:
		journal.log(f"FILE {MAGENTA}{stringFile}{{reset_colour}} NOT FOUND. RETURNING AN EMPTY STRING TO AVOID CRASH.", 3)

		return ""

	except Exception as err:
		journal.log(f"FAILED TO READ {MAGENTA}{stringFile}{{reset_colour}}: {str(err)}", 3)

		return ""

def checkForFolder(path: str) -> None:
	if not os.path.isdir(path):
		os.makedirs(path, exist_ok=True)

		journal.log(f"{SEAFOAM}Setup: {{reset_colour}}Created {MAGENTA}{path}", 5)

def stripURL(url:str) -> str:
	""" Strips invalid characters from URLs """
	safe_chars = ('.','_','-')

	return "".join(c for c in str(url) if c.isalnum() or c in safe_chars).rstrip()

def getCachePath(cog: str) -> str:
	path = CACHE_PATH + "/" + cog

	checkForFolder(path)

	return path

class SafeDict(dict):
	""" Dictionary that returns {key} if a value isn't found for the given key.
	This can be used with string.format_map to only replace template values when
	they exist."""

	def __missing__(self, key):
		return '{' + key + '}'
