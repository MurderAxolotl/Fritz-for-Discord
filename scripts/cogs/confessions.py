import discord
from discord.ext import commands
from resources.shared import CONTEXTS, INTEGRATION_TYPES

class ConfessionView(discord.ui.DesignerView):
	def __init__(self, text="", *, title=None):
		super().__init__(timeout=None)

		container = discord.ui.Container(colour=discord.Colour.blurple())

		if title != None:
			title_text = discord.ui.TextDisplay(f"## {title}")
			container.add_item(title_text)

		body_text = discord.ui.TextDisplay(text)
		container.add_item(body_text)

		super().add_item(container)

class Confessions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	### BOT UTILITIES ###
	@commands.slash_command(name='confess', description='Send an anonymous message to the current channel', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def confess(self, ctx: discord.ApplicationContext, confession=discord.Option(input_type=str, name="your-confession", required=True)):
		try:
			await ctx.send(view=AboutView(confession, title="Confession"))
			await ctx.respond(view=AboutView(confession, title="Confession Recieved"), ephemeral=True)
		except:
			await ctx.respond(view=AboutView("Failed to send confession", title="Something went wrong"), ephemeral=True)