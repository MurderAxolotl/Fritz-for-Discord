import discord
from discord.ext import commands
import json

import sqlite3

import scripts.api.discord as pretty_discord

from resources.sqlite_queries import starboard_queries as queries
import scripts.tools.journal as journal

from resources.shared import CONFIG_PATH
from scripts.tools.utility import getCachePath, stripURL

CACHE_DIR = getCachePath("starboard")


class StarboardView(discord.ui.DesignerView):
	def __init__(self, message: discord.Message):
		super().__init__(timeout=None)

		container = discord.ui.Container(colour=discord.Colour.blurple())
		super().add_item(container)

		title_text = discord.ui.TextDisplay(f"### [New starred message in #{stripURL(message.channel.name)}]({message.jump_url})")
		container.add_item(title_text)

		message_view = discord.ui.Section()
		message_view.set_thumbnail(message.author.display_avatar.url)
		container.add_item(message_view)

		user_name = discord.ui.TextDisplay(f"### {message.author.display_name}")
		message_view.add_item(user_name)

		if message.content:
			body_text = discord.ui.TextDisplay(message.content)
			message_view.add_item(body_text)

		if message.attachments:
			media_gallery = discord.ui.MediaGallery()

			for attachment in message.attachments:
				media_gallery_item = discord.MediaGalleryItem(attachment.url, description=attachment.description, spoiler=attachment.is_spoiler())
				media_gallery.items.append(media_gallery_item)

			container.add_item(media_gallery)


class Starboard(commands.Cog):
	"""
	Just for my own sanity, here's the starboard config schema

	{
		"server_id": {
			"forward_id": "forward_channel_id",
			"starboard_emoji": "starboard_emoji_thingy",
			"count": int_how_many_reactions_before_forwarding,
			"mention": true
		}
	}
	"""

	config = None
	servers = None

	def __init__(self, bot):
		self.bot = bot

		with open(CONFIG_PATH + "/starboard.json", "r") as scf:
			self.config = json.loads(scf.read())

		self.servers = str(self.config.keys()).split("(")[1].split(")")[0]

		# Make sure the table exists in the database
		with self.connect_db() as db:
			self.exec_db(db, queries.create_starboard_cache_table)

	def connect_db(self):
		return sqlite3.connect(CACHE_DIR + "/starboard_cache.db")

	def exec_db(self, connection: sqlite3.Connection, query: str):
		connection.cursor().execute(query)
		connection.commit()

	def read_db(self, connection: sqlite3.Connection, query: str):
		return connection.cursor().execute(query).fetchone()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, ctx: discord.RawReactionActionEvent):
		reactionEmoji = ctx.emoji.name

		if str(ctx.guild_id) not in self.config:
			journal.log(f"Couldn't find starboard information for guild {ctx.guild_id}", 7)

			try:
				fullGuild = await self.bot.fetch_guild(ctx.guild_id)
				journal.log(f"Name: {fullGuild.name}, ID: {fullGuild.id}, Owner: {fullGuild.owner_id}", 7)

			except:
				NotImplemented  # noqa #pyright:ignore

			return

		guildConfig = self.config[str(ctx.guild_id)]
		targetReactionEmoji = guildConfig["starboard_emoji"]

		if reactionEmoji == targetReactionEmoji:
			messageObject = await pretty_discord.get_message(ctx.channel_id, ctx.message_id)
			# Reminder to self: this is a list. Extremely annoying!
			reactions = messageObject["reactions"]

			for reaction_emoji in reactions:
				# Why parse the json properly if it's not something I care about?
				if targetReactionEmoji in str(reaction_emoji):
					if reaction_emoji["count"] >= int(guildConfig["count"]):
						await self.forwardToStarboard(ctx, int(guildConfig["forward_id"]))

	async def forwardToStarboard(self, ctx: discord.RawReactionActionEvent, forwardChannelID: int):
		# Make sure the message hasn't already been starboarded
		with self.connect_db() as db:
			in_starboard = self.read_db(db, queries.search_cache.format(message_id=str(ctx.message_id)))[0]

		if str(in_starboard) == "1":
			return  # Already in starboard, don't do anything

		server = self.bot.get_guild(ctx.guild_id)
		channel = server.get_channel(ctx.channel_id)
		message: discord.Message = await channel.fetch_message(ctx.message_id)

		forward_channel = server.get_channel(forwardChannelID)

		sent_message = await forward_channel.send(view=StarboardView(message))

		with self.connect_db() as db:
			self.exec_db(db, queries.write_cache.format(message_id=str(ctx.message_id), starboard_message_id=str(sent_message.id)))
