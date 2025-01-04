import discord, json

import scripts.api.discord as pretty_discord

from resources.shared import *

with open(PATH + "/config/starboard.json", "r") as scf:
	STARBOARD_CONFIG = json.loads(scf.read())

STARBOARD_SERVERS = str(STARBOARD_CONFIG.keys()).split("(")[1].split(")")[0]

async def reactionAdded(ctx:discord.RawReactionActionEvent, bot:discord.Bot):
	reactionEmoji = ctx.emoji.name
	ctx.guild_id
	targetReactionEmoji = STARBOARD_CONFIG[str(ctx.guild_id)]["starboard_emoji"]

	if reactionEmoji == targetReactionEmoji:
		messageObject = await pretty_discord.get_message(ctx.channel_id, ctx.message_id)
		reactions = messageObject["reactions"] # Reminder to self: this is a list. Extremely annoying!

		for reaction_emoji in reactions:
			if targetReactionEmoji in str(reaction_emoji): # Why parse the json properly if it's not something I care about?
				if reaction_emoji["count"] == int(STARBOARD_CONFIG[str(ctx.guild_id)]["count"]):
					await forwardToStarboard(ctx, bot, int(STARBOARD_CONFIG[str(ctx.guild_id)]["forward_id"]))

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

	SHOULD_PING = bool(STARBOARD_CONFIG[str(ctx.guild_id)]["mention"])

	if str(SERVER_ID) in STARBOARD_SERVERS: # This server has a starboard configured
		if SHOULD_PING: await FORWARD_CHANNEL.send(f"Original post by <@{MESSAGE.author.id}>")
		else: await FORWARD_CHANNEL.send(f"Original post by {AUTHOR}")
		
		await MESSAGE.forward(FORWARD_CHANNEL)



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