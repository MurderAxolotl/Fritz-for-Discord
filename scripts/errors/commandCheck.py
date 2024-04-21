"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

from time import sleep
import discord.ext.commands as commands
import discord

from resources.colour import *

from scripts.tools.utility import *

async def on_command_error(ctx, error):
	# delay_time = 10
	delay_time = -1

	try:
		if isinstance(error, commands.NotOwner) or isinstance(error, swiperNoSwipingError): await ctx.respond("Insufficient permission to execute command")
		elif isinstance(error, commands.BotMissingPermissions): await ctx.respond("The bot has insufficient permission to execute the command. Please double-check that all permissions were granted and try again"); delay_time = -1

		elif isinstance(error, aprilfools): await ctx.respond(f"You know what? I'm done being nice. FUCK YOU, {str(ctx.author).upper()}. I NEVER LIKED YOUR ATTITUDE, YOU LiTTLE SHIT. LEAVE ME ALONE AND NEVER SPEAK AGAIN")
		
		elif isinstance(error, bannedFromNSFW): await ctx.respond("NSFW content generation has been disabled for this server	"); return

		elif isinstance(error, bannedUser): await ctx.respond("You are banned from using Fritz"); return
		
		elif isinstance(error, commands.errors.CheckFailure): await ctx.respond('Failed one or more command checks - you are not allowed to run this command')
		
		elif isinstance(error, commands.errors.MissingRequiredArgument): await ctx.respond("Looks like you forgot to provide a value for {parama}. Try filling out all required fields first!".format(parama=error))

		else:
			await ctx.respond("[ERROR] - Failed to execute command, check log for more details")
			print(MAGENTA + "[Commands] " + RED + "[ERROR] - Failed to execute command: " + str(error) + RESET)

		try: 
			if delay_time != -1: await ctx.delete(delay=delay_time)
		except: NotImplemented

	except Exception as err:
		try: 
			await ctx.respond("[ERROR] - Failed to execute command, check log for more details")
			print(MAGENTA + "[Commands] " + RED + "[ERROR] - While handling an error, another one occured: " + str(err) + RESET)
			
		except Exception as err2:
			print(MAGENTA + "[Commands]" + RED + " [ERROR] - Too many errors occured while attempting to handle another error" + RESET)
			print(MAGENTA + "[Commands]" + YELLOW + " [WARN] - Assuming repeated errors were caused by Discord" + RESET)
			print(RED + "   -> %s"%str(err) + RESET)
			print(RED + "   -> %s"%str(err2) + RESET)

			return
		
	return