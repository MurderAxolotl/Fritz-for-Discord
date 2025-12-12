"""Handles setup on the first startup. Simply importing the module is enough"""

from resources.shared import PATH, PLUGIN_PATH, CONFIG_PATH

from scripts.tools.utility import checkForFolder

checkForFolder(PATH + "/logs")
checkForFolder(PATH + "/logs/system")
checkForFolder(PATH + "/logs/guilds")
checkForFolder(PATH + "/logs/users")
checkForFolder(CONFIG_PATH)
checkForFolder(PLUGIN_PATH)
