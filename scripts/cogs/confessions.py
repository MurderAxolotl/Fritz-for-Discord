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

class Confessions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	### BOT UTILITIES ###
	@commands.slash_command(name='bug', description='Report a bug', contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def bugreport(self, ctx: discord.ApplicationContext):
		await ctx.respond(view=AboutView(loadString("/bug_report").format(GITHUB_BASE=GIT_URL), title="Bug Report"), ephemeral=True)