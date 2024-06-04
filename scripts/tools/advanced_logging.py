import os, datetime

from resources.shared import PATH

def _dateTime() -> str:
	"""Get the current date and time"""
	time = datetime.datetime.now().strftime("%H:%M:%S")
	date = datetime.date.today()

	return str(date) + " " + str(time) + " "

def log2f(log_file_name:str, logtext):
	"""Log to `logs/system/log_file_name.log`"""
	raise NotImplementedError("Currently not needed. Will be implemented once useful")


### Shortcuts
class quick:
	def log_assistant(ctx, prompt):
		user = str(ctx.author).split("#")[0]

		if not os.path.isfile(PATH + "/logs/system/assistant.log"): file = open(PATH + "/logs/system/assistant.log", "x")
		else: file = open(PATH + "/logs/system/assistant.log", "a")

		file.write("\n" + _dateTime() + user + ": " + prompt)
		file.close()

	def log_general(ctx, command, prompt):
		user = str(ctx.author).split("#")[0]

		if not os.path.isfile(PATH + "/logs/system/commands.log"): file = open(PATH + "/logs/system/commands.log", "x")
		else: file = open(PATH + "/logs/system/commands.log", "a")

		file.write("\n" + _dateTime() + user + " " + command + ": " + prompt)
		file.close()

	def logText(command, text):
		if not os.path.isfile(PATH + "/logs/system/commands.log"): file = open(PATH + "/logs/system/commands.log", "x")
		else: file = open(PATH + "/logs/system/commands.log", "a")

		file.write("\n" + _dateTime() + command + ": " + text)
		file.close()