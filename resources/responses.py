import sys, discord
from resources.shared import version, IS_DEBUGGING
import os, platform

from scripts.tools.utility import loadString

# Various messages used by fritz
class help_messages():

	about_system = loadString("/about").format(fritzVersion=version, prodEdition="Production" if not IS_DEBUGGING else "Experimental", backend=(platform.platform(True) + " " + platform.architecture()[0] + " (" + platform.machine() + ") "), cwd=os.getcwd(), pyVer=platform.python_version())
  
	with open(sys.path[0] + "/resources/docs/changelog", "r") as clfile: changelog = discord.File(sys.path[0] + "/resources/docs/changelog")


	MACHINE_LEARNING_NOTICE = r"""
	### MACHINE LEARNING NOTICE
	This command used machine learning, which is extremely harmful to the environment.

	Some eye-opening statistics:
	* Every 100 characters generated uses ~3 bottles of water
	* A single prompt will use approximately 1,500% more power than a single Google search	
	* Google's Machine Learning data centres use more power than the entirety of Ireland
	* 1 percent of all power used worldwide is used by Machine Learning data centres

	Due to environmental concerns, Fritz's ML commands will no longer function. They will be removed <t:1733023608:R> (approximately)

	Thank you for your understanding, and we apologise for the inconvenience

	"""