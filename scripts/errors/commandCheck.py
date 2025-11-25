"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import discord.ext.commands as commands

import scripts.tools.journal as journal

from resources.shared import GIT_URL
from resources.colour import RED, DRIVES, YELLOW, SPECIALDRIVE, BLUE, RESET, MAGENTA, SEAFOAM
from scripts.tools.utility import  swiperNoSwipingError, bannedUser

async def on_command_error(ctx, error):
	try:
		if isinstance(error, commands.NotOwner) or isinstance(error, swiperNoSwipingError):
			await ctx.respond("Only the operator may run this command")

		elif isinstance(error, commands.BotMissingPermissions):
			await ctx.respond("Fritz has insufficient permission to execute the command. Please re-invite Fritz and grant all requested permissions")

		elif isinstance(error, bannedUser):
			await ctx.respond("You are blacklisted from using Fritz")
			journal.log("Blacklisted user attempted to use Fritz: " + str(error), 5)

			return

		elif isinstance(error, commands.errors.CheckFailure):
			await ctx.respond('Failed one or more command checks - you are not allowed to run this command')
			journal.log("Generic check failure detected: " + str(error), 5)

		elif isinstance(error, commands.errors.MissingRequiredArgument):
			await ctx.respond("Looks like you forgot to provide a value for {parama}. Try filling out all required fields first!".format(parama=error))

		elif isinstance(error, NotImplementedError):
			await ctx.respond("This feature is not implemented yet")

		else:
			await ctx.respond(f"Failed to execute command. Please [report this bug](<{GIT_URL}/issues/new?assignees=&labels=bug%2Cbroken+command&projects=&template=broken_command.yml>)")
			journal.log("Failed to execute command: " + str(error), 3)

			print(RED + "[ERROR] - Failed to execute command: " + str(error) + RESET)

	except Exception as err:
		try:
			journal.log("While handling an error, another one occured: " + str(err))

		except Exception as err2:
			print(MAGENTA + "[Commands]" + RED + " [ERROR] - Too many errors occured while attempting to handle another error" + RESET)
			print(MAGENTA + "[Commands]" + YELLOW + " [WARN] - Assuming repeated errors were caused by Discord" + RESET)
			print(RED + "   -> %s"%str(err) + RESET)
			print(RED + "   -> %s"%str(err2) + RESET)

			journal.log("Command caused cascading errors!", 2)

			return

	return
