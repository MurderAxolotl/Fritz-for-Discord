import discord
import json

from resources.shared import CONFIG_PATH

from scripts.tools.utility import getCachePath

CACHE_DIR = getCachePath("starboard")

try:
	import sqlite3

	from sqlite3 import Error as sqlite_error

	import scripts.api.discord as pretty_discord

	from resources.sqlite_queries import starboard_queries as queries

	from resources.shared import *
	from scripts.tools.journal import log

	with open(CONFIG_PATH + "/starboard.json", "r") as scf:
		starboard_config = json.loads(scf.read())

	starboard_servers = str(starboard_config.keys()).split("(")[1].split(")")[0]

	def connect_db():
		return sqlite3.connect(CACHE_DIR + "/starboard_cache.db")

	def exec_db(connection:sqlite3.Connection, query:str):
		connection.cursor().execute(query)
		connection.commit()

	def read_db(connection:sqlite3.Connection, query:str):
		return connection.cursor().execute(query).fetchone()

	async def reload(ctx):
		""" Reloads the configuration from disk """
		global starboard_config, starboard_servers

		with open(CONFIG_PATH + "/starboard.json", "r") as scf:
			starboard_config = json.loads(scf.read())

		starboard_servers = str(starboard_config.keys()).split("(")[1].split(")")[0]

	async def reactionAdded(ctx:discord.RawReactionActionEvent, bot:discord.Bot):
		reactionEmoji = ctx.emoji.name
		if ctx.guild_id not in starboard_config:
			log(f"Couldn't find starboard information for guild {ctx.guild_id}")

			try:
				fullGuild = await bot.fetch_guild(ctx.guild_id)
				log(f"Name: {fullGuild.name}, ID: {fullGuild.id}, Owner: {fullGuild.owner_id}")

			except:
				NotImplemented #noqa #pyright:ignore

			return
		targetReactionEmoji = starboard_config[str(ctx.guild_id)]["starboard_emoji"]

		if reactionEmoji == targetReactionEmoji:
			messageObject = await pretty_discord.get_message(ctx.channel_id, ctx.message_id)
			reactions = messageObject["reactions"] # Reminder to self: this is a list. Extremely annoying!

			for reaction_emoji in reactions:
				if targetReactionEmoji in str(reaction_emoji): # Why parse the json properly if it's not something I care about?
					if reaction_emoji["count"] == int(starboard_config[str(ctx.guild_id)]["count"]):
						await forwardToStarboard(ctx, bot, int(starboard_config[str(ctx.guild_id)]["forward_id"]))

	async def forwardToStarboard(ctx:discord.RawReactionActionEvent, bot:discord.Bot, forwardChannelID:int):
		SERVER_ID  = ctx.guild_id
		CHANNEL_ID = ctx.channel_id
		MESSAGE_ID = ctx.message_id

		FORWARD_CHANNEL_ID = forwardChannelID

		SERVER = bot.get_guild(SERVER_ID)
		CHANNEL = SERVER.get_channel(CHANNEL_ID)
		MESSAGE:discord.Message = await CHANNEL.fetch_message(MESSAGE_ID)

		AUTHOR = str(MESSAGE.author).split("#")[0]

		FORWARD_CHANNEL = SERVER.get_channel(forwardChannelID)

		SHOULD_PING = bool(starboard_config[str(ctx.guild_id)]["mention"])

		if str(SERVER_ID) in starboard_config: # This server has a starboard configured
			with connect_db() as db:
				inStarboard = read_db(db, queries.search_cache.format(message_id=str(ctx.message_id)))[0]

			if str(inStarboard) == "1":
				return # Already in starboard, don't do anything`

			if SHOULD_PING: await FORWARD_CHANNEL.send(f"Original post by <@{MESSAGE.author.id}>")
			else: await FORWARD_CHANNEL.send(f"Original post by {AUTHOR}")

			await MESSAGE.forward(FORWARD_CHANNEL)

			with connect_db() as db:
				exec_db(db, queries.write_cache.format(message_id=str(MESSAGE_ID)))

	# Make sure the table exists in the database
	with connect_db() as db:
		exec_db(db,  queries.create_starboard_cache_table)

	NOQB = False

	########
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

except Exception as err:
	from scripts.tools.journal import log

	NOQB = True
	log("Starboard is unavailable: " + str(err), 4)
