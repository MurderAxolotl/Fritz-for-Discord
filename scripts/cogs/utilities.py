import discord
from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES
from resources.shared import GIT_URL, INVITE_URL, IS_ANDROID, IS_DEBUGGING
from resources.shared import DISALLOW_SYSINF_LEAKS, DISALLOW_PLATFORM_LEAKS, REGISTERED_DEVELOPERS
from resources.responses import help_messages

from scripts.tools.utility import loadString

class AboutView(discord.ui.DesignerView):
	def __init__(self, text="", *, title=None):
		super().__init__(timeout=None)

		container = discord.ui.Container(colour=discord.Colour.blurple())

		if title != None:
			title_text = discord.ui.TextDisplay(f"## {title}")
			container.add_item(title_text)

		body_text = discord.ui.TextDisplay(text)
		container.add_item(body_text)

		super().add_item(container)

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	### BOT UTILITIES ###
	@commands.slash_command(name='bug', description='Report a bug', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def bugreport(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView(loadString("/bug_report").format(GITHUB_BASE=GIT_URL), title="Bug Report"), ephemeral=True)
	
	@commands.slash_command(name='ping', description='Get Fritz\'s current ping', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def ping(self, ctx: discord.ApplicationContext):
		latency = round(self.bot.latency * 1000)
		await ctx.respond(view=AboutView('Current latency: ' + str(latency) + "ms", title="Ping"))

	### INFORMATION COMMANDS ###
	@commands.slash_command(name="help", description="Stop and RTFM", pass_context=True, contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def help(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView(loadString("/commands"), title="Commands"), ephemeral=True)

	@commands.slash_command(name="changelog", description="See past changes to Fritz", pass_context=True, contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def changelog(self, ctx: discord.ApplicationContext):
		await ctx.respond(file=help_messages.changelog, ephemeral=True)

	## Get info about Fritz ##
	@commands.slash_command(name="system", description="Advanced system info", pass_context=True, contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def sysinfo(self, ctx: discord.ApplicationContext):
		if DISALLOW_SYSINF_LEAKS and not (str(ctx.author.id) in REGISTERED_DEVELOPERS): #noqa
			await ctx.respond("You are not allowed to run this command")
			return

		response = help_messages.about_system # Base text

		if not DISALLOW_PLATFORM_LEAKS:
			if IS_ANDROID  : response = response + "\n" + loadString("/android/command_flare")
			if IS_DEBUGGING: response = response + "\n" + loadString("/debug/command_flare")

		await ctx.respond(view=AboutView(response, title="System Info"), ephemeral=True)

	@commands.slash_command(name="about", description="Learn more about Fritz", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def sysabout(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView(help_messages.about_fritz, title="About"))

	@commands.slash_command(name='invite', description='Get Fritz\'s invite URL', pass_context=True, contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def getInvite(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView("-# NOTE: This link is to add Fritz to a SERVER. To add it to an account, you need to click \"Add App\" in Fritz's profile\n" + INVITE_URL, title="Invite URL"), ephemeral=True)

	@commands.slash_command(name='git_url', description='Get Fritz\'s Git URL', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def getGit(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView(GIT_URL, title="Git URL"))

