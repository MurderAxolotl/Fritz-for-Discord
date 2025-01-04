""" Ensures configs actually exist on the system """
""" Must be run after firstRun, otherwise this will fail"""

import os

from resources.shared import PATH
from resources.colour import *

CONFIG_DIR = PATH + "/config"

def createBlankConfig(path):
	with open(path, "x") as blankConfig:
		blankConfig.write(r"{}")

if not os.path.isdir(CONFIG_DIR): print(RED + "[ConfigCreator] WARN: config dir does not exist! Creating it now" + RESET)
if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR); print(SEAFOAM + "ConfigCreator: Created /config" + RESET)

# Actually start creating the configs. They will be blank by default and must be filled by the user
if not os.path.isfile(CONFIG_DIR + "/starboard.json"): createBlankConfig(CONFIG_DIR + "/starboard.json")