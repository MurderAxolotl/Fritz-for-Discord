import requests
import asyncio
import json

import discord
from discord.ext import commands

import scripts.tools.journal as journal
from resources.shared import CONTEXTS, INTEGRATION_TYPES, CONFIG_PATH

LOG_COMPONENT = "Quotebook"


class QuotebookModal(discord.ui.DesignerModal):
	def __init__(self, message: discord.Message, webhook):
		super().__init__(title="Quotebook Message")

		self.message = message
		self.message_text = self.message.content
		self.author_name = self.message.author.display_name
		self.avatar_url = self.message.author.display_avatar.url
		self.webhook = webhook

		message_text_display = discord.ui.TextDisplay(self.message_text)
		super().add_item(message_text_display)

	async def callback(self, interaction: discord.Interaction):
		form = {
			"content": f"{self.message_text}",
			"username": f"{self.author_name} (via Fritz)",
			"avatar_url": f"{self.avatar_url}"
		}

		try:
			request = requests.post(self.webhook, json=form)
			request.raise_for_status()

			await interaction.response.send_message("Quotebooked", ephemeral=True)
		except HTTPError as http_error:
			journal.log(f"Discord returned error {http_error.code}: {http_error.reason}", 4, component=LOG_COMPONENT)

			await interaction.response.send_message("Failed to quotebook!", ephemeral=True)


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
		try:
			server = ctx.guild.id

		except: #noqa
			server = 0

		if str(server) in self.guild_list:
			modal = QuotebookModal(message=message, webhook=self.config[str(server)]["channel"])
			await ctx.send_modal(modal)

		else:
			await ctx.respond("Quotebook is not enabled here", ephemeral=True)

