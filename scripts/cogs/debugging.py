from inspect import Parameter
import discord
from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES

from scripts.tools import journal
from scripts.tools.utility import bannedUser, isDeveloper, swiperNoSwipingError

# Implemented exception types
IMPLEMENTED_EXCEPTIONS = ["NotOwner", "SwiperNoSwipingError", "BotMissingPermissions", "BannedUser", "CheckFailure", "MissingRequiredArgument", "ExtensionAlreadyLoaded", "ExtensionNotFound", "ExtensionError", "NoEntryPointError", "ExtensionFailed"]

class DebugView(discord.ui.DesignerView):
	def __init__(self, text="", *, title=None):
		super().__init__(timeout=None)

		container = discord.ui.Container(colour=discord.Colour.blurple())

		if title != None:
			title_text = discord.ui.TextDisplay(f"## {title}")
			container.add_item(title_text)

		body_text = discord.ui.TextDisplay(text)
		container.add_item(body_text)

		super().add_item(container)

class Debug(commands.Cog):
	debugCommandGroup = discord.SlashCommandGroup("dbg", "Debug commands", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)

	def __init__(self, bot: discord.Bot):
		self.bot = bot

	@debugCommandGroup.command(name='throw_exception', description='Intentionally throw an exception', contexts=CONTEXTS, integration_tpyes=INTEGRATION_TYPES)
	@isDeveloper()
	async def throw_exception(
		self,
		ctx: discord.ApplicationContext,
		exception_type:discord.Option(str, choices=IMPLEMENTED_EXCEPTIONS, description="The type of exception")
	):
		match exception_type:
			case "NotOwner"               : raise commands.NotOwner
			case "SwiperNoSwipingError"   : raise swiperNoSwipingError
			case "BotMissingPermissions"  : raise commands.BotMissingPermissions(["Legit permission error, totally"])
			case "BannedUser"             : raise bannedUser
			case "CheckFailure"           : raise commands.errors.CheckFailure
			case "MissingRequiredArgument": raise commands.errors.MissingRequiredArgument(Parameter("LegitParameter", Parameter.POSITIONAL_ONLY))
			case "ExtensionAlreadyLoaded" : raise discord.ExtensionAlreadyLoaded("LegitExtension")
			case "ExtensionNotFound"      : raise discord.ExtensionNotFound("LegitExtension")
			case "ExtensionError"         : raise discord.ExtensionError("Forced Exception", name="LegitExtension")
			case "NoEntryPointError"      : raise discord.NoEntryPointError("LegitExtension")
			case "ExtensionFailed"        : raise discord.ExtensionFailed("LegitExtension", Exception("Forced exception"))

			case _                        : raise Exception("Unknown exception type lmfao??")

	@debugCommandGroup.command(name='walk_commands', description='Dumps a list of all commands', contexts=CONTEXTS, integration_Types=INTEGRATION_TYPES)
	@isDeveloper()
	async def dump_all_commands(self, ctx: discord.ApplicationContext):
		await ctx.defer(ephemeral=True)

		commandList = self.bot.walk_application_commands()
		commands = []

		full_string = "## Available commands: "

		try:
			while True:
				commands.append(next(commandList))

		except Exception:
			pass

		for command in commands:
			if isinstance(command, discord.commands.core.SlashCommand):
				full_string = full_string + f"\n**{command.name}** - {command.description}"

		await ctx.respond(full_string)
