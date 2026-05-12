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
		self.webhook = webhook

		self.message_text = self.message.content
		self.author_name = self.message.author.display_name
		self.avatar_url = self.message.author.display_avatar.url

		message_text_display = discord.ui.TextDisplay(self.message_text)
		super().add_item(message_text_display)

	async def callback(self, interaction: discord.Interaction):
		await self.webhook.send(
			content=self.message_text,
			username=f"{self.author_name} (via Fritz)",
			avatar_url=self.avatar_url,
		)

		await interaction.response.send_message("Quotebooked", ephemeral=True)


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
			guild_id = ctx.guild.id

		except: #noqa
			guild_id = 0

		if str(guild_id) in self.guild_list:
			channel_id=self.config[str(guild_id)]["channel_id"]

			server = self.bot.get_guild(guild_id)
			channel = server.get_channel(channel_id)

			# If channel isn't already cached, fetch it from Discord
			if channel is None:
				journal.log(f"Couldn't find channel {channel_id} in cache, fetching from Discord", 7, component=LOG_COMPONENT)
				channel = await self.bot.fetch_channel(channel_id)

			webhook = await self.get_or_create_webhook(channel)

			modal = QuotebookModal(message=message, webhook=webhook)
			await ctx.send_modal(modal)

		else:
			await ctx.respond("Quotebook is not enabled here", ephemeral=True)

	async def get_or_create_webhook(self, channel: discord.TextChannel):
		# Check for existing webhooks
		webhooks = await channel.webhooks()
		for webhook in webhooks:
			if webhook.user == self.bot.user:
				return webhook

		journal.log(f"Couldn't find existing webhook for {channel.name}, creating new one", 7, component=LOG_COMPONENT)
		# If we don't find an existing webhook, create a new one
		return await channel.create_webhook(name="Fritz Quotebook")

