import os, sys, datetime

import scripts.tools.utility as utility
from resources.colour import *

async def logMessage(message):
	
	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M:%S")
	today = datetime.date.today()
	unit = None

	if await utility.check(message) == True: 
		guild_id = str(message.author).split("#0", 1)[0]

		logPath = sys.path[0] + "/logs/users/%s.log"%(guild_id)

	else: 
		try: guild_id = str(message.guild.id)
		except: 
			print(RED + "Guild cache needs to be refreshed. Message will not be logged" + RESET)
			return -1
		
		channel_id = str(message.channel.id)

		logPath = sys.path[0] + "/logs/guilds/%s/%s.log"%(guild_id, channel_id)

		if not os.path.isdir(sys.path[0] + "/logs/guilds/%s"%(guild_id)):
			print(YELLOW + "Creating dir %s"%sys.path[0] + "/logs/guilds/%s"%(guild_id))
			os.mkdir(sys.path[0] + "/logs/guilds/%s"%(guild_id))

	fs = str(today) + " " + str(current_time) + " "
	messageContent = str(message.author).split("#0")[0] + ": " + message.content

	if (os.path.isfile(logPath)): log = open(logPath, "a")
	else: log = open(logPath, "+x")

	log.write(fs + messageContent + "\n")
	log.close()