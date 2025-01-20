""" Ensures configs actually exist on the system """
""" Must be run after firstRun, otherwise this will fail"""

import os

from resources.shared import journal
from resources.shared import PATH
from resources.colour import *

CONFIG_DIR = PATH + "/config"

def verify(path:str):
	if not os.path.isfile(CONFIG_DIR + path): createBlankConfig(path)

def createBlankConfig(path):
	with open(CONFIG_DIR + path, "x") as blankConfig:
		blankConfig.write(r"{}")

if not os.path.isdir(CONFIG_DIR): 
	print(RED + "[ConfigCreator] WARN: config dir does not exist! Creating it now" + RESET)
	journal.log("ConfigCreator: config dir does not exist! Creating it now", 4)

	os.mkdir(CONFIG_DIR)

# Actually start creating the configs. They will be blank by default and must be filled by the user
verify("/starboard.json")