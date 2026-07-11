from discord.ext import commands


class Module(commands.Cog):
	repo_url: str | None
	new_issue_url: str | None
