"""
Original code created by MurderAxolotl.
Please give credit. Source: https://github.com/psychon-night/Fritz-for-Discord
"""

import os
import discord

import scripts.tools.journal as journal

from resources.shared import PTK_FOLDER
from resources.colour import RED, RESET

# Generate sprite lists

if (PTK_FOLDER != "") and (PTK_FOLDER is not None):
	for directory in os.listdir(PTK_FOLDER):
		inventory = []

		for file in os.listdir(f"{PTK_FOLDER}/{directory}"):
			inventory.append(file)

		match directory:
			case "artemis": ARTEMIS = inventory #noqa
			case "rofi"   : ROFI    = inventory #noqa
			case "theo"   : THEO    = inventory #noqa
			case "hunter" : HUNTER  = inventory #noqa
			case "friend" : FRIEND  = inventory #noqa
			case "ollie"  : OLLIE   = inventory #noqa
			case _        :
				print(f"{RED}[PTK_REACTIONS] Unrecognized character: {directory}{RESET}")
				journal.log(f"[PTK_REACTIONS] Unrecognized character: {directory}")


async def reaction_image(ctx: discord.ApplicationContext, character:str, sprite_name:str):
	await ctx.defer()

	sprite_path = f"{PTK_FOLDER}/{character.lower()}"

	await ctx.respond(file=discord.File(filename=sprite_name, fp=f"{sprite_path}/{sprite_name}"))
