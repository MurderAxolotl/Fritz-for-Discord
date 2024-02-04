""" Provides custom triggers for specific words """

import os, sys, string

illegal = ""

def sanitiseInput(input:str):
	global illegal

	final = ""

	for char in input:
		if char.lower() in string.ascii_letters + " ": final = final + char
		else: illegal = illegal + char

	return final

async def createKeyword(ctx, triggerWord, content):
	global illegal 

	targetFile = sys.path[0] + "/resources/docs/lyrics/" + sanitiseInput(triggerWord)

	if not os.path.exists(targetFile):
		file = open(targetFile, "x")
		file.write(content)
		file.close()

		if illegal == "": await ctx.channel.send("INTERNAL_FLAG::::__update_lyrcache", silent=True); return "Reaction phrase created"
		else: return "Reaction phrase created; stripped illegal chars: %s"%illegal

	else: return "Reaction phrase already exists"

async def deleteKeyword(ctx, triggerWord):
	targetFile = sys.path[0] + "/resources/docs/lyrics/" + sanitiseInput(triggerWord)

	if os.path.exists(targetFile): 
		os.remove(targetFile)

		await ctx.channel.send("INTERNAL_FLAG::::__update_lyrcache")

		return "Reaction phrase removed"

	else: return "Reaction phrase not found"

async def readKeyword(triggerWord):
	targetFile = sys.path[0] + "/resources/docs/lyrics/" + sanitiseInput(triggerWord)

	if os.path.exists(targetFile):
		content = open(targetFile, "r").read()

		if len(content) > 2000: return "Response phrase too long, it must be replayed by triggering the keyword"
		return content

	else: return "Reaction phrase not found"

async def listKeywords(): return str(os.listdir(sys.path[0] + "/resources/docs/lyrics/"))

async def editKeyword(triggerWord, newContent):
	targetFile = sys.path[0] + "/resources/docs/lyrics/" + sanitiseInput(triggerWord)

	if os.path.exists(targetFile): 
		file = open(targetFile, "w")
		file.truncate(0); file.seek(0)
		file.write(newContent)
		file.close()

		return "Reaction phrase updated"

	else: return "Reaction phrase not found"