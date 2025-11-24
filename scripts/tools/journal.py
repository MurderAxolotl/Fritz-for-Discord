import datetime
import os
import sys

from resources.shared import PATH
from resources.colour import RED, DRIVES, YELLOW, RESET

LOG_SEVERITY = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG"]

""" Log to the journal file and stdout\n
Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info, 7=debug`
"""

def _log_to_disk(message:str, severity:int=6):
	LOG_LOC = PATH + "/logs/journal"

	template = "{date}@{time} - [{sev}] {entry}\n"

	current_time = datetime.datetime.now().strftime("%H:%M:%S")
	today = datetime.date.today()

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))

def _log_to_stdout(message:str, print_colour:str="", severity:int=6):
	""" Write a log message\n
	Severity: `0=emergency, 1=alert, 2=critical, 3=error, 4=warning, 5=notice, 6=info`\n
	If `print_colour` is not set:
		- 0, 1, 2, 3: message is red
		- 4: message is yellow
		- 5: message is orange
		- 6, 7: message is white
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
	
	output_text = print_colour + template.format(sev=LOG_SEVERITY[severity], entry=message) + RESET

	# Output errors to stderr
	if severity <= 3:
		print(output_text, file=sys.stderr)
	else:
		print(output_text, file=sys.stdout)

def ___lognoprefix(message:str, severity:int=6):
	LOG_LOC = PATH + "/logs/journal"
	
	print(message)

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(message + "\n")
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(message + "\n")

def log(message:str, severity:int=6):
	""" Write a log message\n
	Severity: `0=emergency, 1=alert, 2=critical, 3=error, 4=warning, 5=notice, 6=info, 7=debug`
	"""

	_log_to_stdout(message, severity=severity)
	_log_to_disk(message, severity)

def log_fatal(message:str):
	""" Logs at the CRITICAL level """
	log(message, 2)
