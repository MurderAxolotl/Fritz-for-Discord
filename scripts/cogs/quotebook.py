import requests
import asyncio
import json

import discord
from discord.ext import commands

import scripts.tools.journal as journal
from resources.shared import CONTEXTS, INTEGRATION_TYPES
from resources.shared import QUOTE_WEBHOOK, QUOTE_ID, CONFIG_PATH


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

			request = requests.post(dynamic_webhook, json = form)

		else:
			request = requests.post(QUOTE_WEBHOOK, json = form)

		if request.status_code != "200":
			journal.log(f"Discord returned error {request.status_code}: {request.text}", 4, component="Quotebook")

		await ctx.respond("Quotebooked", ephemeral=True)

