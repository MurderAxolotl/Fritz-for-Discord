import requests
import asyncio
import json

import discord
from discord.ext import commands

import scripts.tools.journal as journal
from resources.shared import CONTEXTS, INTEGRATION_TYPES, CONFIG_PATH

LOG_COMPONENT = "Quotebook"


class Quotebook(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		# Load quotebook config
		with open(f"{CONFIG_PATH}/quotebook.json", "r") as qconfig:
			self.config = json.loads(qconfig.read())

		self.guild_list = []

		if self.config != "{}":
			for guild in self.config:
				self.guild_list.append(guild)

	@commands.message_command(name="Quotebook", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)
	async def quotebook(self, ctx: discord.ApplicationCommand, message: discord.Message):
		await ctx.defer(ephemeral=True)

		author_name = message.author.display_name
		message_text = message.content
		avatar_url = message.author.display_avatar.url

		try:
			server = ctx.guild.id

		except: #noqa
			server = 0

		try:
			form = {
				"content": f"{message_text}",
				"username": f"{author_name} (via Fritz)",
				"avatar_url": f"{avatar_url}"
			}

		except: #noqa
			form = {
				"content": f"{message_text}",
				"username": f"{author_name} (via Fritz)"
			}

		if str(server) in self.guild_list:
			dynamic_webhook = self.config[str(server)]["channel"]

			try:
				request = requests.post(dynamic_webhook, json = form)
				request.raise_for_status()
			except HTTPError as http_error:
				journal.log(f"Discord returned error {http_error.code}: {http_error.reason}", 4, component=LOG_COMPONENT)

			await ctx.respond("Quotebooked", ephemeral=True)

		else:
			await ctx.respond("Quotebook is not enabled here", ephemeral=True)

