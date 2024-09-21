""" Tool to update the current version of Fritz. Desktop version. """

import os
from resources.colour import *
from resources.shared import PATH

BASE_URL = "https://raw.githubusercontent.com/psychon-night/Fritz-for-Discord/refs/heads/main/"

def downloadUpdate():
	""" Downloads and installs core updates """

	# Ensure the core is updated
	os.system(f"cd {PATH} && wget -q --show-progress --progress=bar:force {BASE_URL}/main.py")
	os.system(f"cd {PATH} && wget -q --show-progress --progress=bar:force {BASE_URL}/commands_bridge.py")
	os.system(f"cd {PATH} && wget -q --show-progress --progress=bar:force {BASE_URL}/fupdate.py")

	# Now the scary clobber-y part!

	for directory in os.listdir(PATH):
		if os.path.isdir(f"{PATH}/{directory}") and not "cache" in directory:

			for file in os.listdir(f"{PATH}/{directory}"):
				if not "__" in file:
					if os.path.isfile(f"{PATH}/{directory}/{file}"): 
						os.system(f"cd {PATH}/{directory} && wget -q --show-progress --progress=bar:force {BASE_URL}/{directory}/{file}")

					else: 
						for actual_files in os.listdir(f"{PATH}/{directory}/{file}"): 
							if not "__" in file: 
								os.system(f"cd {PATH}/{directory}/{file} && wget -q --show-progress --progress=bar:force {BASE_URL}/{directory}/{file}/{actual_files}")

	print(SPECIALDRIVE + "Finished" + RESET)


wgetReady = input(BLUE + "Is wget installed? [Y/N] > ").lower()

if wgetReady == "n": print(YELLOW + "Run 'sudo apt install wget' and try again" + RESET)
elif wgetReady == "y": downloadUpdate()
else: print(RED + "Invalid option" + RESET)