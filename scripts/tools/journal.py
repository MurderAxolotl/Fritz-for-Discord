import datetime
import os
import systemd.journal as systemd

from resources.shared import PATH

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

def log(message:str, severity:int=6):
	""" Write a log message\n
	Severity: `0=emergency, alert=1, 2=critical, 3=error, 4=warning, 5=notice, 6=info`
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
