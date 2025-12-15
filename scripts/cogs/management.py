import discord
from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES

from scripts.tools import journal
from scripts.tools.utility import isDeveloper

class ManagementView(discord.ui.DesignerView):
	def __init__(self, text="", *, title=None, success=True):
		super().__init__(timeout=None)

		container = discord.ui.Container(colour=discord.Colour.green() if success else discord.Colour.red())

		if title != None:
			title_text = discord.ui.TextDisplay(f"## {title}")
			container.add_item(title_text)

		body_text = discord.ui.TextDisplay(text)
		container.add_item(body_text)

		super().add_item(container)

class Management(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(name='loadplugin', description='Loads a plugin', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	@isDeveloper()
	async def load_plugin(self, ctx: discord.ApplicationContext, *, plugin_name: str):
		await ctx.defer()

		module_name = f"{plugin_name}.plugin"
		journal.log(f"User {ctx.user} attempting to load plugin {plugin_name}", 5)

		self.bot.load_extension(module_name)

		journal.log(f"Plugin {plugin_name} loaded", 5)
		await ctx.respond(view=ManagementView(f"Loaded plugin `{plugin_name}`", title="Load Plugin", success=True))

	@commands.slash_command(name='unloadplugin', description='Unloads a plugin', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	@isDeveloper()
	async def unload_plugin(self, ctx: discord.ApplicationContext, *, plugin_name: str):
		await ctx.defer()

		module_name = f"{plugin_name}.plugin"
		journal.log(f"User {ctx.user} attempting to unload plugin {plugin_name}", 5)

		self.bot.unload_extension(module_name)

		journal.log(f"Plugin {plugin_name} unloaded", 5)
		await ctx.respond(view=ManagementView(f"Unloaded plugin `{plugin_name}`", title="Unload Plugin", success=True))

	@commands.slash_command(name='reloadplugin', description='Reloads a plugin', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	@isDeveloper()
	async def reload_plugin(self, ctx: discord.ApplicationContext, *, plugin_name: str):
		await ctx.defer()

		module_name = f"{plugin_name}.plugin"
		journal.log(f"User {ctx.user} attempting to reload plugin {plugin_name}", 5)

		self.bot.reload_extension(module_name)

		journal.log(f"Plugin {plugin_name} reloaded", 5)
		await ctx.respond(view=ManagementView(f"Reloaded plugin `{plugin_name}`", title="Reload Plugin", success=True))
