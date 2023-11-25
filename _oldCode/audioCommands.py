import random
import string
from time import sleep
from scripts.tools.utility import *

connectedVC = None
audioQueue = []
audioPlaying = False
currentAudioLink = None
leaveAfterFinish = False

async def playAudio(ctx: discord.ApplicationContext, youtube_link, channel_id, audible_keepalive, bot):
	global audioQueue, audioPlaying, currentAudioLink, leaveAfterFinish, connectedVC
	dl_required = 1
	sleptFor = 0
	audioQueue.append(youtube_link)

	leaveAfterFinish = False
	
	await ctx.defer()

	if audioPlaying: return

	res = await ctx.respond("Caching audio...")
	audioPlaying = True

	try: voice = await bot.fetch_channel(channel_id)
	except: return await ctx.respond("Invalid voice channel ID")

	try: connectedVC = await voice.connect()
	except: return await ctx.respond("Unable to establish audio gateway")

	while len(audioQueue) != 0 or leaveAfterFinish == False:
		while len(audioQueue) == 0: 
			await asyncio.sleep(1.0)
			currentItem = None
			if not audible_keepalive: connectedVC.send_audio_packet(b'0')
			else: connectedVC.send_audio_packet(b'A very nifty keepalive signal; a few packets will be sent'); connectedVC.send_audio_packet(b'e#rE3E3')
			if leaveAfterFinish: 
				await connectedVC.disconnect()
				await res.edit("Finished playing")
				audioPlaying = False
				currentAudioLink = None
				return 0

		currentItem = audioQueue[0]
		currentAudioLink = currentItem

		if dl_required == 1: 
			print(YELLOW + "Downloading %s"%currentItem + RESET)
			await downloadYoutubeVideo(currentItem, 5)

		try: 
			audioFile = discord.FFmpegOpusAudio(source="/home/lexi/Documents/Fritz/cache/video_cache.opus")
			await res.edit("Playing `%s`"%await getPageTitle(currentItem))
		except: 
			await res.edit("Failed to load ffmpeg audio stream, skipping to next queue item")
			os.system("rm /home/lexi/Documents/Fritz/cache/video_cache.opus")
		
		if os.path.isfile("/home/lexi/Documents/Fritz/cache/video_cache.opus"):
			try:
				connectedVC.play(audioFile)
				print("sdfadfasdfasfdasdfasdfasdfasdfasdfasdfasdf")
			except:
				await ctx.channel.send("Unable to read audio stream for %s, skipping to next track!"%await getPageTitle(currentItem))
		else: await ctx.channel.send("Error reading unknown audio stream, skipping to next track!")

		while connectedVC.is_playing():
			await asyncio.sleep(1)

		audioQueue.pop(0)

		if len(audioQueue) == 0: os.system("rm /home/lexi/Documents/Fritz/cache/video_cache.opus")
		else:
			if not (audioQueue[0] == currentItem):
				os.system("rm /home/lexi/Documents/Fritz/cache/video_cache.opus"); dl_required = 1

			else: print(RED + "Not erasing" + RESET); dl_required = 0

	try:
		await connectedVC.disconnect()
		await res.edit("Finished playing")
		audioPlaying = False
		currentAudioLink = None
	except: NotImplemented

async def addQueue(ctx: discord.ApplicationContext, youtube_link):
	global audioQueue, audioPlaying

	title = await getPageTitle(youtube_link)

	if audioPlaying:
		audioQueue.append(youtube_link)
		await ctx.respond("Added `%s` to queue!"%title)
	else:
		await ctx.respond("No player instance exists. use `play_audio` instead")
	

async def removeQueue(ctx, queue_item_number:int):
	global audioQueue

	await ctx.defer()
	itemTarget = queue_item_number
	
	if itemTarget == -1:
		firstItem = audioQueue[0]
		audioQueue.clear()
		audioQueue.append(firstItem)

	elif (itemTarget >= 1):
		audioQueue.pop(itemTarget)

async def getQueue(ctx):
	global currentAudioLink
	if currentAudioLink != None:
		await ctx.defer()
		queueLength = len(audioQueue)
		numEmbeded = 0

		contextOutput = discord.Embed(title="Queue", description="There are currently %s items queued"%str(queueLength), colour=discord.Colour.dark_purple(),)

		contextOutput.add_field(name="", value="%s [playing]"% await getPageTitle(currentAudioLink), inline=False)
		contextOutput.add_field(name="", value="# ============== #", inline=False)

		for song in audioQueue:
			if numEmbeded <= 9:
				songTitle = await getPageTitle(song)
				contextOutput.add_field(name="", value=songTitle, inline=False)
				numEmbeded += 1

		contextOutput.set_footer(text="Only up to the next 9 queued items will be shown")
			
		await ctx.respond(embed=contextOutput)

	else:
		await ctx.respond("No queue can possibly exist; audio player is not spawned")

async def stopTrack(ctx):
	global connectedVC
	
	connectedVC.stop()
	await ctx.respond("Skipped track")

async def pauseToggle(ctx):
	global connectedVC

	isPaused = connectedVC.is_paused()

	if isPaused: connectedVC.resume(); await ctx.respond("Unpaused")
	else: connectedVC.pause(); await ctx.respond("Paused. Use the `pause_play` command again to resume")

async def allowLeave(ctx):
	global leaveAfterFinish

	await ctx.defer()
	leaveAfterFinish = True

	await ctx.respond("Issued disconnect request")

async def immediateLeave(ctx):
	global connectedVC, leaveAfterFinish, audioQueue
	await ctx.defer()

	if connectedVC != None:
		leaveAfterFinish = True
		audioQueue.clear()

		connectedVC.stop()
		connectedVC.disconnect()

	await ctx.respond("Issued forced disconnect command")

async def getDebugInfo(ctx):
	global audioPlaying, audioQueue, connectedVC, currentAudioLink, leaveAfterFinish

	contextOutput = discord.Embed(title="Audio Debugger", description="Fritz Audio Debugger", colour=discord.Colour.brand_red(),)

	contextOutput.add_field(name="", value="instance: %s"%str(connectedVC), inline=False)
	if connectedVC != None:
		contextOutput.add_field(name="", value="is_playing: %s"%connectedVC.is_playing(), inline=False)
		contextOutput.add_field(name="", value="is_paused: %s"%connectedVC.is_paused(), inline=False)
	contextOutput.add_field(name="", value="current_file: <%s>"%currentAudioLink, inline=False)
	contextOutput.add_field(name="", value="leaveAfterFinish: %s"%leaveAfterFinish, inline=False)
	contextOutput.add_field(name="", value="queue_length: %s"%str(len(audioQueue)), inline=False)

	contextOutput.set_footer(text="Fritz Embedded Audio Debugger (FEAD)")

	await ctx.respond(embed=contextOutput)

def audioSocketSyncTestLoader():
	global connectedVC
	if connectedVC != None:
		for i in range(0,25): connectedVC.send_audio_packet('FFFFFFFFF')
		sleep(1)
		randstring = ""
		for i in range(0,500):
			for i in range(0,random.randint(1,25)): randstring = randstring + random.choice(string.digits + string.ascii_letters + string.punctuation)
			connectedVC.send_audio_packet(bytes(randstring, "utf-8"))
			randstring = ""
		sleep(1)
		for i in range(0,25): connectedVC.send_audio_packet('5555555')

	
	else: NotImplemented

async def audioSocketSyncTest(ctx):
	await ctx.defer()
	await loop.run_in_executor(ThreadPoolExecutor(), lambda: audioSocketSyncTestLoader())
	await ctx.respond("Socket test complete")

def rawPacketLoader(count, autoPause:bool, data):
	global connectedVC
	counted = 0
	should_resume = False

	if connectedVC != None:
		if not connectedVC.is_paused() and autoPause: connectedVC.pause(); should_resume = True
		try:
			while count != counted:
				randstring = data
				for i in range(0,random.randint(1,25)): randstring = randstring + random.choice(string.digits + string.ascii_letters + string.punctuation)

				connectedVC.send_audio_packet(bytes(randstring, "utf-8"))
				counted += 1
				randstring = ""

		except Exception as err:
			# print(str(err))
			try:connectedVC.send_audio_packet(bytes(str(err), "utf-8"))
			except:NotImplemented

	else:
		NotImplemented

	if should_resume: connectedVC.resume()

async def rawPacket(ctx, count, autopause, data):
	await ctx.defer()
	await loop.run_in_executor(ThreadPoolExecutor(), lambda: rawPacketLoader(count, autopause, data))
	await ctx.respond("Raw packets were transmitted", ephemeral=True)