from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES
from scripts.tools import journal
from scripts.api.module import Module

from .config import *


class ExamplePlugin(Module):
	name = NAME
	repo_url = REPO_URL
	new_issue_url = NEW_ISSUE_URL

	# Test command
	@commands.slash_command(name="hello", description="Say hi to the bot!", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def hello(self, ctx):
		journal.log(f"User {ctx.user} said hi!", 6, component=NAME)
		await ctx.respond(f"HIIIII {ctx.author.display_name.upper()}")


def setup(bot):
	bot.add_cog(ExamplePlugin(bot))


def teardown(bot):
	bot.remove_cog("ExamplePlugin")
