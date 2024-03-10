import sys
from resources.shared import version
import os, platform

# Various messages used by fritz
class help_messages():
	commands = """The following commands are currently supported:
  **\# API INTERACTION #**
  **assistant** *<prompt>*: talk to Fritz, ask him questions, and perform other tasks
  **pp_users** *<search term>*: search PronounsPage for a username
  **pp_terms** *<search term>*: search PronounsPage for terminology
  **seasify** 	*<query>* *[count]*: Search Spotify for *query* and return *count* results. Count must be between 1 and 25
  **cai** *<message>* *<character>*: Send *message* to the *character* and get their response. This FULLY supports chat history!
  
  **\# FUN #**
  **givecat**: get a random cat image (from the internet)
  **joke**: get a random joke (from the internet)
  **quote**: get a random quote (from the internet)
  **quoteme**: get a random quote from you in the current channel

  **\# KEYWORDS #**
  **create** *<phrase> <response>*: Create a new trigger. Like Carl-Bot's little quirps thing
  **delete** *<phrase>*: Deletes <phrase>
  **read** *<phrase>*: Manually trigger the phrase and play-back the content
  **edit** *<phrase> <new content>*: Replaces the content of <phrase> with <new content>
  **list**: Lists available keywords

  **\# QR TOOLS \#**
  **scan_qr** *<imageURL>*: scan the image at *image URL* and process any readable QR Codes
  **create_qr** *<content>* *[style]*: Create a QR code. The "style" controls appearance and ECC levels, defaulting to *stylized*

  **\# BOT MANAGEMENT #**
  **ping**: test the bot's latency

  **\#\# INFORMATION ##**
  **about**:  send some basic information about Fritz
  **help**:   send a list of supported commands
  **system**: get Fritz's backend information
  **invite**: get the bot's invite URL

  **\#\# OTHER COMMANDS ##**
  **initiate_dm**: start a DM between the current user and Fritz

  *Options surrounded by <angle brackets> are required*
  *Options surrounded by [square brackets] are optional*
  """


	about = """Fritz | Simple utility bot for Chaos Incorporated

  Current version: **{ver}**
  Current prefix: *Depricated*

  To get started, run /help
  """.format(ver=version)


	about_system = """Fritz | *Bringing chaos for over a year*

  Current version: **{ver}**

  Backend: **{backend}**
  Python Version: {pyVer}
  CWD: **{cwd}**
""".format(ver=version, backend=(platform.platform(True) + " " + platform.architecture()[0] + " (" + platform.machine() + ") "), cwd=os.getcwd(), pyVer=platform.python_version())
  
	with open(sys.path[0] + "/resources/docs/changelog", "r") as clfile: changelog = clfile.read()