import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from resources.shared import CONTEXTS, INTEGRATION_TYPES
from resources.shared import GIT_URL, INVITE_URL, IS_ANDROID, IS_DEBUGGING
from resources.shared import DISALLOW_SYSINF_LEAKS, DISALLOW_PLATFORM_LEAKS, REGISTERED_DEVELOPERS
from resources.responses import help_messages

from scripts.tools.utility import loadString

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	command_group = SlashCommandGroup("f_u", "Fritz's basic utility commands", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)

	### BOT UTILITIES ###
	@command_group.command(name='bug', description='Report a bug')
	async def bugreport(self, ctx: discord.ApplicationContext):
		await ctx.respond(loadString("/bug_report").format(GITHUB_BASE=GIT_URL), ephemeral=True)
	
	@command_group.command(name='ping', description='Get Fritz\'s current ping')
	async def ping(self, ctx: discord.ApplicationContext):
		latency = round(self.bot.latency * 1000)
		await ctx.respond('Current latency: ' + str(latency) + "ms")

	### INFORMATION COMMANDS ###
	@command_group.command(name="help", description="Stop and RTFM", pass_context=True)
	async def help(self, ctx: discord.ApplicationContext):
		await ctx.respond(loadString("/commands"), ephemeral=True)

	@command_group.command(name="changelog", description="See past changes to Fritz", pass_context=True)
	async def changelog(self, ctx: discord.ApplicationContext):
		await ctx.respond(file=help_messages.changelog, ephemeral=True)

	## Get info about Fritz ##
	@command_group.command(name="system", description="Advanced system info", pass_context=True)
	async def sysinfo(self, ctx: discord.ApplicationContext):
		if DISALLOW_SYSINF_LEAKS and not (str(ctx.author.id) in REGISTERED_DEVELOPERS): #noqa
			await ctx.respond("You are not allowed to run this command")
			return

		response = help_messages.about_system # Base text

		if not DISALLOW_PLATFORM_LEAKS:
			if IS_ANDROID  : response = response + "\n" + loadString("/android/command_flare")
			if IS_DEBUGGING: response = response + "\n" + loadString("/debug/command_flare")

		await ctx.respond(response, ephemeral=True)

	@command_group.command(name="about", description="Learn more about Fritz")
	async def sysabout(self, ctx: discord.ApplicationContext):
		await ctx.respond(help_messages.about_fritz)

	@command_group.command(name='invite', description='Get Fritz\'s invite URL', pass_context=True)
	async def getInvite(self, ctx: discord.ApplicationContext):
		await ctx.respond("NOTE: This link is to add Fritz to a SERVER. To add it to an account, you need to click \"Add App\" in Fritz's profile\n" + INVITE_URL, ephemeral=True)

	@command_group.command(name='git_url', description='Get Fritz\'s Git URL')
	async def getGit(self, ctx: discord.ApplicationContext):
		await ctx.respond(GIT_URL)

