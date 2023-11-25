import sys
from resources.shared import version
import os, platform

# Various messages used by fritz
class help_messages():
	commands = """The following commands are currently supported:
  **\# API INTERACTION #**
  **chatgpt** *<prompt>*: interact with Fritz's language model
  **pp_users** *<search term>*: search PronounsPage for a username
  **pp_terms** *<search term>*: search PronounsPage for terminology
  **mj** *<prompt>* *[style]*: Use an open-source MidJourney model to generate some art
  **diffuse** *<prompt>* *[style]*: Use an open-source Stable Diffusion model to generate some art
  **goodporn** *<prompt>* *[style]*: Use an open-source MJ/SD model to... you know
  **seasify** 	*<query>* *[count]*: Search Spotify for *query* and return *count* results. Count must be between 1 and 25
  **cai** *<message>* *<character>*: Send *message* to the *character* and get their response. This FULLY supports chat history!
  **givecat**: get a random cat image (from the internet)
  **joke**: get a random joke (from the internet)

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