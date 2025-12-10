from discord.ext import commands

from resources.shared import CONTEXTS, INTEGRATION_TYPES
from scripts.tools import journal

LOG_COMPONENT = "Example Plugin"

# Test command
@commands.slash_command(name="hello", description="Say hi to the bot!", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
async def hello(ctx):
	journal.log(f"User {ctx.user} said hi!", 6, component=LOG_COMPONENT)

	await ctx.respond(f"HIIIII {ctx.author.display_name.upper()}")

def setup(bot):
    bot.add_application_command(hello)

def teardown(bot):
	journal.log("BYEEEEE!!!", 5, component=LOG_COMPONENT)
