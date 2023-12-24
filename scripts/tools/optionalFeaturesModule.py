class config():
	blockImages = False
	enableCrazy = False

async def imageBanModule(message):
	""" Prevents emojis and images from being sent """
	try:
		print(message.content)
		if "<:" in str(message.content): await message.delete()
		if "Screenshot" in message.attachments[0].url: await message.delete()
		await message.delete()

	except Exception as err: print(str(err))

async def crazyOnce(message):
	""" Fritz was crazy once. Crazy? Fritz was crazy once. Crazy? Fritz was crazy once. Crazy? Fritz was crazy once. Crazy? Fritz wa- """
	if "crazy" in str(message.content).lower() and not "Fritz" in str(message.author):
		await message.channel.send("Crazy?")
		await message.channel.send("I was crazy once")
		await message.channel.send("They locked me in a room")
		await message.channel.send("A rubber room")
		await message.channel.send("A rubber room with rats")
		await message.channel.send("And rats make me crazy")