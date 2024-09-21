async def createSentenceFromMyStuff(ctx, loop, sample_size, guild_id, chan_id):
	if isinstance(ctx.guild, NoneType) and guild_id == -1: 
		await ctx.respond("Please move to a guild or provide a guild_id"); return
	await ctx.defer()

	if isinstance(ctx.guild, NoneType) and chan_id == -1: await ctx.respond("You also need to provide a channel_id"); return

	if guild_id == -1: guild_id = ctx.guild.id
	if chan_id == -1: chan_id = ctx.channel.id

	words = []
	userMessages = []
	guildDir = sys.path[0] + f"/logs/guilds/{str(guild_id)}"
	selectedLog = open(guildDir + f"/{chan_id}.log", "r")
	uname = str(ctx.author).split("#")[0]

	for message in selectedLog.readlines():
		if uname in message: 
			userMessages.append(message)

	if len(userMessages) == 0: 
			await ctx.respond("Couldn't get any quotes. Try again, maybe?")
			return

	for i in range(0, sample_size):
		msg = userMessages[random.randint(0,len(userMessages)-1)]
		msg = msg.split(maxsplit=2)
		oncesaid = str(msg[2]).split(":", maxsplit=1)[1]

		words.append(oncesaid.split(" ", maxsplit=2)[1].strip())

	string = str(words).replace("[", "").replace("]", "")

	print(YELLOW + "Selected words: " + string + RESET)

	await gpt.generateResponse(ctx, "Write a short story using all of these words: %s"%string, loop, "turbo")