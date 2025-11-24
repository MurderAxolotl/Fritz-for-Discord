import datetime
import os
import sys

from resources.shared import PATH
from resources.colour import RED, DRIVES, YELLOW, RESET

LOG_SEVERITY = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG"]

""" Log to the journal file and stdout\n
Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info, 7=debug`
"""

def _log_to_disk(message:str):
	LOG_LOC = PATH + "/logs/journal"

	template = "{date}@{time} {entry}\n"

	current_time = datetime.datetime.now().strftime("%H:%M:%S")
	today = datetime.date.today()

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))

def _log_to_stdout(message:str, severity:int=6):
	# Output errors to stderr
	if severity <= 3:
		print(message, file=sys.stderr, flush=True)
	else:
		print(message, file=sys.stdout, flush=True)

def ___lognoprefix(message:str, severity:int=6):
	LOG_LOC = PATH + "/logs/journal"
	
	print(message, flush=True)

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(message + "\n")
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(message + "\n")

def log(message:str, severity:int=6, print_colour:str=""):
	""" Write a log message\n
	Severity: `0=emergency, 1=alert, 2=critical, 3=error, 4=warning, 5=notice, 6=info, 7=debug`
	If `print_colour` is not set:
		- 0, 1, 2, 3: message is red
		- 4: message is yellow
		- 5: message is orange
		- 6, 7: message is white
	`{reset_colour}` can be used in the message to reset back to the `print_colour`.
	"""

	template = "fritz[{sev}]: {entry}"

	if print_colour == "":
		match severity:
			case 0|1|2|3:
				print_colour = RED
			case 4:
				print_colour = YELLOW
			case 5:
				print_colour = DRIVES
			case 6|7:
				print_colour = RESET
	
	output_text = print_colour + template.format(sev=LOG_SEVERITY[severity], entry=message.format(reset_colour=print_colour)) + RESET

	_log_to_stdout(output_text, severity=severity)
	_log_to_disk(output_text)

def log_fatal(message:str):
	""" Logs at the CRITICAL level """
	log(message, 2)
