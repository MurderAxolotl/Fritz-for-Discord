import discord

from resources.shared import intents


class activities():
	halloween = discord.Activity(name = "Halloween", 
		state = "HAPPY SPOOKY DAY", 
		type=discord.ActivityType.competing, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)

	spookyMonth = discord.Activity(name = "Goulish Screams", 
		state = "IT'S SPOOKY MONTH >:3", 
		type=discord.ActivityType.listening, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	christmas = discord.Activity(name = "Yiffmas", 
		state = "Merry Yiffmas!", 
		type=discord.ActivityType.competing, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	standard = discord.Activity(name = "the world burn", 
		state = "The flames bring me joy...", 
		type=discord.ActivityType.watching, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)
	
	screamingChildren = discord.Activity(
		name = "screaming children", 
		state = "Their screams make me happy...", 
		type=discord.ActivityType.listening, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)

	generic = discord.Activity(
		name = " ", 
		state = "", 
		type=discord.ActivityType.listening, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)

	debug = discord.Activity(
		name = "DEBUG MODE", 
		state = "Fritz is running in debug mode. Features may be broken", 
		type=discord.ActivityType.playing, 
		assets={'large_image':'foxfox', 'large_text':'gay'}, 
		application_id=1070042394009014303
	)


class Holiday:
	halloween = [
		discord.Client(activity=activities.halloween, intents=intents, log_level=None, log_handler=None), 
		"Spooky Day"
	]

	spooky = [
		discord.Client(activity=activities.spookyMonth, intents=intents, log_level=None, log_handler=None), 
		"Spooky Season"
	]


	christmas = [
		discord.Client(activity=activities.christmas, intents=intents, log_level=None, log_handler=None), 
		"Christmas"
	]


class Default:
	none = [
		discord.Client(activity=activities.generic, intents=intents, log_level=None, log_handler=None), 
		"none"
	]

	debug = [
		discord.Client(activity=activities.debug, intents=intents, log_level=None, log_handler=None), 
		"Debug"
	]

	standard = [
		discord.Client(activity=activities.standard, intents=intents, log_level=None, log_handler=None), 
		"Default"
	]

	screamingChildren = [
		discord.Client(activity=activities.screamingChildren, intents=intents, log_level=None, log_handler=None), 
		"Screaming Children"
	]