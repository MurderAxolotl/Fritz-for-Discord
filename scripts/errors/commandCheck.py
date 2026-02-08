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
		# Check if error has an "original" parameter -- was running into issues without this
		if "original" in dir(error):
			mappedError = error.original

		else:
			mappedError = error

	except Exception:
		mappedError = error

	try:
		if isinstance(mappedError, commands.NotOwner) or isinstance(error, swiperNoSwipingError):
			await ctx.respond("Only the operator may run this command", ephemeral=True)

		elif isinstance(mappedError, commands.BotMissingPermissions):
			await ctx.respond("Fritz has insufficient permission to execute the command. Please re-invite Fritz and grant all requested permissions", ephemeral=True)

		elif isinstance(mappedError, bannedUser):
			journal.log(f"Blacklisted user attempted to use Fritz: {str(error)}", 5)
			await ctx.respond("You are blacklisted from using Fritz", ephemeral=True)

			return

		elif isinstance(mappedError, commands.errors.CheckFailure):
			journal.log(f"Generic check failure detected: {str(error)}", 5)
			await ctx.respond('Failed one or more command checks - you are not allowed to run this command', ephemeral=True)

		elif isinstance(mappedError, commands.errors.MissingRequiredArgument):
			await ctx.respond(f"Looks like you forgot to provide a value for {str(error)}. Try filling out all required fields first!", ephemeral=True)

		# === Extensions ===
		elif isinstance(mappedError, discord.ExtensionNotFound):
			journal.log("Extension {error.original.name} not found", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` not found", title="Load Plugin", success=False), ephemeral=True)

		elif isinstance(mappedError, discord.ExtensionNotLoaded):
			journal.log(f"Extension {error.original.name} not loaded", 4)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` not loaded", title="Load Plugin", success=False), ephemeral=True)

		elif isinstance(mappedError, discord.ExtensionAlreadyLoaded):
			journal.log(f"Extension {error.original.name} already loaded", 4)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` already loaded", title="Load Plugin", success=False), ephemeral=True)

		elif isinstance(mappedError, discord.NoEntryPointError):
			journal.log(f"Extension {error.original.name} has no entrypoint", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` failed to load: No entrypoint", title="Load Plugin", success=False), ephemeral=True)

		elif isinstance(mappedError, discord.ExtensionFailed):
			journal.log(f"Extension {error.original.name} failed to load: {str(error.original.original)}", 3)
			await ctx.respond(view=ManagementView(f"Extension `{error.original.name}` failed to load: `{str(error.original.original)}", title="Load Plugin", success=False), ephemeral=True)

		else:
			journal.log("Failed to execute command: " + str(error), 3)
			await ctx.respond(f"Failed to execute command. Please [report this bug](<{GIT_URL}/issues/new?assignees=&labels=bug%2Cbroken+command&projects=&template=broken_command.yml>)", ephemeral=True)

	except Exception as err:
		journal.log(f"While handling an error, another one occured: {str(err)}", 3)

	return
