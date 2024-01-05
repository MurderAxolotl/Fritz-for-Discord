import string
illegalChars = ""

class config():
	blockImages = False
	enableCrazy = True

async def imageBanModule(message):
	""" Prevents emojis and images from being sent """
	try:
		print(message.content)
		if "<:" in str(message.content): await message.delete()
		if "Screenshot" in message.attachments[0].url: await message.delete()
		if len(message.attachments) != 0: await message.delete()
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

async def gay(message):
	if "gay" in str(message.content).lower() and not "Fritz" in str(message.author):
		await message.channel.send("Gay?")
		await message.channel.send("I was gay once")
		await message.channel.send("They locked me in a room")
		await message.channel.send("A rubber room")
		await message.channel.send("A rubber room with boys")
		await message.channel.send("And boys make me gay")

async def banUgly(message):
	global illegalChars
	c = str(message.content).lower()
	con = c.replace(" ", "")
	newString = ""
	lastChar = ""

	for char in con:
		if char in string.ascii_lowercase and char != lastChar:
			newString = newString + char
			lastChar = char

	try: 
		if message.attachments[0].url == "https://cdn.discordapp.com/attachments/1170875047376851035/1189776992699158568/image.png" or "image.png" in message.attachments[0].url or "age" in message.attachments[0].url or "png" in message.attachments[0].url: await message.delete()
		try: await message.attachments[0].delete()
		except Exception as err: print(str(err))
	except: NotImplemented

	if "ugly" in newString or "uly" in newString or "ugy" in newString or "ugl" in newString or "gly" in newString or "ulgy" in newString or "imso" in newString or "imthe" in newString or "im" in newString or "iam" in newString or "i" in newString or "מְכוֹעָר" in newString or "me" in newString or "am" in newString:
		await message.delete()

	if "terrible look" in c or "bad look" in c or "disgusting" in c or "so awful" in c or "looking" in c or "hid" in c or "dis" in c:
		await message.delete()

	# elif "bjoink" in str(message.author) and ("u" in c or "g" in c or "l" in c or "y" in c):
	# 	await message.delete()
		
async def absolute_solver(message):
	await message.delete()