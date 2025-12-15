import discord
from discord.ext import commands
import json

import sqlite3

import scripts.api.discord as pretty_discord

from resources.sqlite_queries import starboard_queries as queries
from resources.shared import PATH
import scripts.tools.journal as journal


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

		with open(PATH + "/config/starboard.json", "r") as scf:
			self.config = json.loads(scf.read())

		self.servers = str(self.config.keys()).split("(")[1].split(")")[0]

		# Make sure the table exists in the database
		with self.connect_db() as db:
			self.exec_db(db, queries.create_starboard_cache_table)

	def connect_db(self):
		return sqlite3.connect(PATH + "/cache/starboard_cache.db")

	def exec_db(self, connection: sqlite3.Connection, query: str):
		connection.cursor().execute(query)
		connection.commit()

	def read_db(self, connection: sqlite3.Connection, query: str):
		return connection.cursor().execute(query).fetchone()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, ctx: discord.RawReactionActionEvent):
		reactionEmoji = ctx.emoji.name

		if str(ctx.guild_id) not in self.config:
			journal.log(f"Couldn't find starboard information for guild {ctx.guild_id}")

			try:
				fullGuild = await self.bot.fetch_guild(ctx.guild_id)
				journal.log(f"Name: {fullGuild.name}, ID: {fullGuild.id}, Owner: {fullGuild.owner_id}")

			except:
				NotImplemented  # noqa #pyright:ignore

			return

		guildConfig = self.config[str(ctx.guild_id)]
		targetReactionEmoji = guildConfig["starboard_emoji"]
		ping = bool(guildConfig["mention"])

		if reactionEmoji == targetReactionEmoji:
			messageObject = await pretty_discord.get_message(ctx.channel_id, ctx.message_id)
			# Reminder to self: this is a list. Extremely annoying!
			reactions = messageObject["reactions"]

			for reaction_emoji in reactions:
				# Why parse the json properly if it's not something I care about?
				if targetReactionEmoji in str(reaction_emoji):
					if reaction_emoji["count"] == int(guildConfig["count"]):
						await self.forwardToStarboard(ctx, int(guildConfig["forward_id"]), ping)

	async def forwardToStarboard(self, ctx: discord.RawReactionActionEvent, forwardChannelID: int, ping: bool):
		SERVER_ID = ctx.guild_id
		CHANNEL_ID = ctx.channel_id
		MESSAGE_ID = ctx.message_id

		SERVER = self.bot.get_guild(SERVER_ID)
		CHANNEL = SERVER.get_channel(CHANNEL_ID)
		MESSAGE: discord.Message = await CHANNEL.fetch_message(MESSAGE_ID)

		AUTHOR = str(MESSAGE.author).split("#")[0]

		FORWARD_CHANNEL = SERVER.get_channel(forwardChannelID)

		# Make sure the message hasn't already been starboarded
		with self.connect_db() as db:
			inStarboard = self.read_db(db, queries.search_cache.format(message_id=str(ctx.message_id)))[0]

		if str(inStarboard) == "1":
			return  # Already in starboard, don't do anything`

		if ping:
			await FORWARD_CHANNEL.send(f"Original post by <@{MESSAGE.author.id}>")
		else:
			await FORWARD_CHANNEL.send(f"Original post by {AUTHOR}")

		await MESSAGE.forward_to(FORWARD_CHANNEL)

		with self.connect_db() as db:
			self.exec_db(db, queries.write_cache.format(message_id=str(MESSAGE_ID)))
