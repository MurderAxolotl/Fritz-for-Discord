"""Handles setup on the first startup. Simply importing the module is enough"""

import os

from resources.shared import PATH, CACHE_PATH, PLUGIN_PATH
from resources.colour import YELLOW, MAGENTA, SEAFOAM, RESET

import scripts.tools.journal as journal

def checkForFolder(path:str) -> None:
	if not os.path.isdir(path):
		os.mkdir(f"{path}")

		journal.log(f"{SEAFOAM}Setup: {{reset_colour}}Created {MAGENTA}{path}", 5)


checkForFolder(PATH + "/logs")
checkForFolder(PATH + "/logs/system")
checkForFolder(PATH + "/logs/guilds")
checkForFolder(PATH + "/logs/users")
checkForFolder(CACHE_PATH)
checkForFolder(CACHE_PATH + "/qr")
checkForFolder(PATH + "/config")
checkForFolder(PLUGIN_PATH)
