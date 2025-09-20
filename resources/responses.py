import sys
import discord
from resources.shared import BOOTID, VERSION, IS_DEBUGGING
import os
import platform

from scripts.tools.utility import loadString

# Various messages used by fritz
class help_messages():

	about_system = loadString("/about").format(fritzVersion=VERSION, prodEdition="Stable" if not IS_DEBUGGING else "Experimental", backend=(platform.platform(True) + " " + platform.architecture()[0] + " (" + platform.machine() + ") "), cwd=os.getcwd(), pyVer=platform.python_version(), BOOT_ID=BOOTID)
	about_fritz = loadString("/basic_about").format(fritzVersion=VERSION, prodEdition="Stable" if not IS_DEBUGGING else "Experimental")

	with open(sys.path[0] + "/resources/docs/changelog", "r") as clfile: changelog = discord.File(sys.path[0] + "/resources/docs/changelog")
