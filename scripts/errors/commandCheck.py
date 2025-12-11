"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import discord
import discord.ext.commands as commands

import scripts.tools.journal as journal

from resources.shared import GIT_URL
from resources.colour import RED, DRIVES, YELLOW, SPECIALDRIVE, BLUE, RESET, MAGENTA, SEAFOAM
from scripts.tools.utility import swiperNoSwipingError, bannedUser
from scripts.cogs.management import ManagementView

async def on_command_error(ctx, error):
	try:
		if isinstance(error.original, commands.NotOwner) or isinstance(error, swiperNoSwipingError):
			await ctx.respond("Only the operator may run this command")

		elif isinstance(error.original, commands.BotMissingPermissions):
			await ctx.respond("Fritz has insufficient permission to execute the command. Please re-invite Fritz and grant all requested permissions")

		elif isinstance(error.original, bannedUser):
			journal.log("Blacklisted user attempted to use Fritz: " + str(error), 5)
			await ctx.respond("You are blacklisted from using Fritz")

			return

		elif isinstance(error.original, commands.errors.CheckFailure):
			journal.log("Generic check failure detected: " + str(error), 5)
			await ctx.respond('Failed one or more command checks - you are not allowed to run this command')

		elif isinstance(error.original, commands.errors.MissingRequiredArgument):
			await ctx.respond("Looks like you forgot to provide a value for {parama}. Try filling out all required fields first!".format(parama=error))

		# === Extensions ===
		elif isinstance(error.original, discord.ExtensionNotFound):
			journal.log("Extension {error.original.name} not found", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` not found", title="Load Plugin", success=False))

		elif isinstance(error.original, discord.ExtensionNotLoaded):
			journal.log(f"Extension {error.original.name} not loaded", 4)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` not loaded", title="Load Plugin", success=False))

		elif isinstance(error.original, discord.ExtensionAlreadyLoaded):
			journal.log(f"Extension {error.original.name} already loaded", 4)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` already loaded", title="Load Plugin", success=False))

		elif isinstance(error.original, discord.NoEntryPointError):
			journal.log(f"Extension {error.original.name} has no entrypoint", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` failed to load: No entrypoint", title="Load Plugin", success=False))

		elif isinstance(error.original, discord.ExtensionFailed):
			journal.log(f"Extension {error.original.name} failed to load: {str(error.original.original)}", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` failed to load: `{str(error.original.original)}", title="Load Plugin", success=False))

		else:
			journal.log("Failed to execute command: " + str(error), 3)
			await ctx.respond(f"Failed to execute command. Please [report this bug](<{GIT_URL}/issues/new?assignees=&labels=bug%2Cbroken+command&projects=&template=broken_command.yml>)")

	except Exception as err:
		try:
			journal.log("While handling an error, another one occured: " + str(err), 3)

		except Exception as err2:
			journal.log("Commands: Too many errors occured while attempting to handle another error. Assuming repeated errors were caused by Discord.", 2)
			journal.log("   -> %s"%str(err), 2)
			journal.log("   -> %s"%str(err2), 2)

			return

	return
