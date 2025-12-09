import dotenv
import discord
import requests
import json
import os
import random

import scripts.tools.journal as journal
from scripts.tools.utility import isDeveloper

from resources.shared import CONTEXTS, INTEGRATION_TYPES, PATH

# Load environment variables
dotenv.load_dotenv("plugins/csa_wheel.env")
WON_KEY = os.getenv("wheel_api_key", "")

# Command groups
fate = bot.create_group("fate", contexts=CONTEXTS, integration_types=INTEGRATION_TYPES)

# Add commands to the command groups
@fate.command(name="spin", description="Spin a wheel")
async def spin_wheel(context):
	try:
		await context.defer()
		is_sane_interaction = True

	except Exception:
		await context.channel.trigger_typing()
		is_sane_interaction = False

	if os.path.isfile(f"{PATH}/cache/csa_wheel"):
		try:
			wheel_config = json.loads(open(f"{PATH}/cache/csa_wheel", "r").read())
			entries = wheel_config["entries"]

			weighted_table = []

			for item in entries:
				for i in range(0, int(item["weight"])):
					weighted_table.append(item["text"])

			if len(weighted_table) > 0:
				if is_sane_interaction:
					await context.respond(random.choice(weighted_table))
				else:
					await context.channel.send(random.choice(weighted_table))

			else:
				await context.respond("Wheel has no valid choices. Are the weights whole numbers?")

		except json.JSONDecodeError as jse:
			journal.log(f"plugin/csa_wheel: Failed to parse wheel data: {jse}", 3)

			await context.respond("Something went wrong while setting up the wheel. Try `set_wheel` again, perhaps?")

	else:
		await context.respond("No wheels are currently loaded. Run the `set_wheel` command to get started")

@fate.command(name="urtest", description="_dev.urtest.random_test_iter")
@isDeveloper()
async def urtest(context, iterations:int=60):
	await context.defer()

	if os.path.isfile(f"{PATH}/cache/csa_wheel"):
		try:
			wheel_config = json.loads(open(f"{PATH}/cache/csa_wheel", "r").read())
			entries = wheel_config["entries"]

			weighted_table = []

			for item in entries:
				for i in range(0, int(item["weight"])):
					weighted_table.append(item["text"])

			results = {}

			if len(weighted_table) > 0:
				for i in range(0, iterations):
					sinstance_result = random.choice(weighted_table)

					if sinstance_result in results:
						results[sinstance_result] += 1

					else:
						results[sinstance_result] = 1

				await context.respond(f"```json\n{results}\n```")

			else:
				await context.respond("Wheel has no valid choices. Are the weights whole numbers?")

		except json.JSONDecodeError as jse:
			journal.log(f"plugin/csa_wheel: Failed to parse wheel data: {jse}", 3)

			await context.respond("Something went wrong while setting up the wheel. Try `set_wheel` again, perhaps?")

	else:
		await context.respond("No wheels are currently loaded. Run the `set_wheel` command to get started")

@fate.command(name="set_weight", description="Set the weight of any entry on the active wheel")
async def set_weight(context, weight:discord.Option(int, description="Weight. Default 5", min_value=1, max_value=10)=1): #type:ignore
	raise NotImplementedError

@fate.command(name="reset_wheel", description="Resets weights for all entries on the active wheel")
async def reset_wheel(context, are_you_really_sure:discord.Option(str, choices=["Confirm"], description="Are you REALLY sure?")): #type:ignore
	if are_you_really_sure:
		raise NotImplementedError

	else:
		await context.respond("Reset cancelled")

@fate.command(name="set_wheel", description="Choose what wheel to set as active")
async def set_wheel(context, wheel_id:discord.Option(str, description="7-character wheel ID", max_length=7)): #type:ignore
	try:
		await context.defer()

		# Oh theo, this is such a bad idea lmao
		wheelResponse = requests.get(f"https://wheelofnames.com/api/v2/wheels/{wheel_id}", headers={"x-api-key": WON_KEY})

		if wheelResponse.status_code != 200:
			journal.log(f"plugin/csa_wheel: set_wheel failed: {wheelResponse.text}", 3)

			await context.respond("Failed to get wheels, API error")
			return

		selectedWheel = json.loads(wheelResponse.text)["data"]["wheelConfig"]

		if os.path.exists(f"{PATH}/cache/csa_wheel"):
			with open(f"{PATH}/cache/csa_wheel", "w") as csa_wheel:
				csa_wheel.truncate(0)
				csa_wheel.seek(0)

				csa_wheel.write(json.dumps(selectedWheel))
				csa_wheel.close()

			wheelName = selectedWheel["title"]

			await context.respond(f"Wheel set to {wheelName}")

		else:
			with open(f"{PATH}/cache/csa_wheel", "x") as csa_wheel:
				csa_wheel.write(str(selectedWheel))
				csa_wheel.close()

			wheelName = selectedWheel["title"]

			await context.respond(f"Wheel set to {wheelName}")

	except json.JSONDecodeError as jde:
		journal.log(f"plugin/csa_wheel: Error processing wheels: {str(jde)}", 3)

		await context.respond("Couldn't understand API's response")

	except Exception as err:
		journal.log(f"plugin/csa_wheel: set_wheel failed: {str(err)}", 3)

		raise err

@fate.command(name="list_wheels", description="Get a list of available wheels")
async def get_wheels(context):
	try:
		await context.defer()

		wheelResponse = requests.get("https://wheelofnames.com/api/v2/wheels", headers={"x-api-key": WON_KEY})

		if wheelResponse.status_code != 200:
			journal.log(f"plugin/csa_wheel: list_wheels failed: {wheelResponse.text}", 3)

			await context.respond("Failed to get wheels, API error")
			return

		wheelObject = json.loads(wheelResponse.text)

		# Get the actual list of wheels
		user_wheels = {}

		for wheel in wheelObject["data"]["wheels"]:
			user_wheels[wheel["wheelConfig"]["title"]] = wheel["path"]

		await context.respond("The following wheels are available: " + str(user_wheels))

	except json.JSONDecodeError as jde:
		journal.log(f"plugin/csa_wheel: Error processing wheels: {str(jde)}", 3)

		await context.respond("Couldn't understand API's response")

	except Exception as err:
		journal.log(f"plugin/csa_wheel: list_wheels failed: {str(err)}", 3)

		raise err

# This overwrites Fritz's default implementation
async def dmstwfunc(message):
	if message.content.lower() == "spin the wheel":
		await spin_wheel(message)

def _funchook() -> tuple[list, list, list]:
	# Signature: [on_ready, on_message, on_error]
	return [], [dmstwfunc], []
