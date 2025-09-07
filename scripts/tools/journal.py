import datetime
import os
import systemd.journal as systemd

from resources.shared import PATH
from resources.colour import RED, DRIVES, YELLOW, RESET

LOG_SEVERITY = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO"]

""" Interface with systemd logs\n
Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info` """
def logDisk(message:str, severity:int=6):
	LOG_LOC = PATH + "/logs/journal"

	template = "{date}@{time} - [{sev}] {entry}\n"

	current_time = datetime.datetime.now().strftime("%H:%M:%S")
	today = datetime.date.today()

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, sev=LOG_SEVERITY[severity], entry=message))

def log_and_print(message:str, print_colour:str="", severity:int=6):
	""" Write a log message\n
	Severity: `0=emergency, 1=alert, 2=critical, 3=error, 4=warning, 5=notice, 6=info`\n
	If `print_colour` is not set:
		- 0, 1, 2, 3: message is red
		- 4, 5: message is orange
		- 6: message is yellow
	"""

	if print_colour == "":
		match severity:
			case 0|1|2|3:
				print_colour = RED
			case 4|5:
				print_colour = DRIVES
			case 6:
				print_colour = YELLOW

	print(print_colour + message + RESET)
	log(message, severity)

def log(message:str, severity:int=6):
	""" Write a log message\n
	Severity: `0=emergency, 1=alert, 2=critical, 3=error, 4=warning, 5=notice, 6=info`
	"""

	logDisk(message, severity)
	systemd.send(message, SYSLOG_IDENTIFIER="fritz", LEVEL=LOG_SEVERITY[severity])

def log_fatal(message:str):
	""" Logs at the CRITICAL level """
	LOG_LOC = PATH + "/logs/journal"

	template = "{date}@{time} - [CRITICAL] {entry}\n"
	current_time = datetime.datetime.now().strftime("%H:%M:%S")
	today = datetime.date.today()

	if os.path.exists(LOG_LOC):
		with open(LOG_LOC, "a") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))
	else:
		with open(LOG_LOC, "x") as log_file: log_file.write(template.format(date=today, time=current_time, entry=message))

	systemd.send(message, SYSLOG_IDENTIFIER="fritz", LEVEL="critical")
