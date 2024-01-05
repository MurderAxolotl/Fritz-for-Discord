import random
import string
from time import sleep

from scripts.tools.utility import *

instances_in_memory = []
instanceMemory = {}

class memoryInstance():
	memoryID = None
	connectedVC = None
	audioQueue = []
	audioPlaying = False
	currentAudioLink = None
	leaveAfterFinish = False

	def __init__(self, mem_id): 
		global instanceMemory, instances_in_memory
		self.memoryID = mem_id
		instanceMemory.update({str(self.memoryID): self})

		instances_in_memory.append(mem_id)


	def set_ID(self, id): self.memoryID = id
	def delItemFromQueue(self): 
		try: self.audioQueue.pop(0)
		except: print("nope")

def removeFromMemory(GUILD_ID):
	global instances_in_memory, instanceMemory
	instances_in_memory.remove(GUILD_ID)
	try:instanceMemory.pop(str(GUILD_ID))
	except: print(instanceMemory)

async def playAudio(ctx: discord.ApplicationContext, youtube_link:str, channel_id:int, audible_keepalive:bool, bot):
	global instances_in_memory, instanceMemory

	download_required = 1
	idle_set = 0
	audio_url = None

	GUILD_ID = ctx.guild.id

	if GUILD_ID in instances_in_memory:
		instance = instanceMemory[str(GUILD_ID)]
		instance.audioQueue.append(youtube_link)
		return
	
	INSTANCE = memoryInstance(GUILD_ID)
	await ctx.defer()
	
	INSTANCE.audioQueue.append(youtube_link)
	INSTANCE.leaveAfterFinish = False

	discord_response = await ctx.respond("Attempting to download audio...")
	INSTANCE.audioPlaying = True

	try: voice_instance = await bot.fetch_channel(channel_id)
	except: 
		removeFromMemory(GUILD_ID)
		return await ctx.respond("Invalid voice channel ID")
	
	try: 
		INSTANCE.connectedVC = await voice_instance.connect()
		connectedVC = INSTANCE.connectedVC
	except:
		removeFromMemory(GUILD_ID)
		return await ctx.respond("Unable to establish connection to voice gateway")
	
	while INSTANCE.leaveAfterFinish == False:
		while len(INSTANCE.audioQueue) == 0:
			# Sleep
			await asyncio.sleep(1.0)
			if idle_set == 0: idle_set = 1; await discord_response.edit("Idle")
			audio_url = None

			if not audible_keepalive: connectedVC.send_audio_packet(b'0')
			else: connectedVC.send_audio_packet(b'A very nifty keepalive signal; a few packets will be sent'); connectedVC.send_audio_packet(b'e#rE3E3')
			if INSTANCE.leaveAfterFinish: 
				await connectedVC.disconnect(); await discord_response.edit("Finished playing")
				removeFromMemory(GUILD_ID)
				return 0
			
		try:audio_url = INSTANCE.audioQueue[0]
		except: audio_url = ""
		INSTANCE.currentAudioLink = audio_url

		if download_required:
			print(YELLOW + "Downloading %s"%audio_url + RESET)
			await downloadYoutubeVideo(audio_url, INSTANCE.memoryID)

		try:
			audioFile = discord.FFmpegOpusAudio(source="/home/%s/Documents/Fritz/cache/video_cache%s.opus"%(os.getlogin(), GUILD_ID))
			await discord_response.edit("Playing `%s`"%await getPageTitle(audio_url))

		except:
			await discord_response.edit("Failed to load ffmpeg audio stream, skipping to next queue item")
			os.system("rm /home/%s/Documents/Fritz/cache/video_cache%s.opus"%(os.getlogin(), GUILD_ID))

		if os.path.isfile("/home/%s/Documents/Fritz/cache/video_cache%s.opus"%(os.getlogin(), GUILD_ID)):
			try: connectedVC.play(audioFile)
			except: await ctx.channel.send("Unable to read audio stream for %s, skipping to next track!"%await getPageTitle(audio_url))
		else: await ctx.channel.send("Error reading unknown audio stream, skipping to next track!")

		while connectedVC.is_playing():
			try: await asyncio.sleep(1)
			except: await ctx.channel.send("Error during playback - attempting to recover...")

		await asyncio.sleep(1) # Delay to fix issues with file descriptor crashes (apparently it takes ffmpeg a second to close the fucking IO)
		# I am going to cry if this doesn't work

		try: INSTANCE.delItemFromQueue()
		except: print(RED + "Empty list encountered" + RESET)
		print(len(INSTANCE.audioQueue))

		if len(INSTANCE.audioQueue) == 0: 
			os.system("rm /home/%s/Documents/Fritz/cache/video_cache%s.opus"%(os.getlogin(), GUILD_ID))
			print(RED + "Removing file" + RESET)
		else:
			if not (INSTANCE.audioQueue[0] == audio_url):
				os.system("rm /home/%s/Documents/Fritz/cache/video_cache%s.opus"%(os.getlogin(), GUILD_ID)); download_required = 1
				print(RED + "Removing file" + RESET)

			else: print(RED + "Not erasing" + RESET); download_required = 0

	try:
		removeFromMemory(GUILD_ID)

		await connectedVC.disconnect()
		await discord_response.edit("Finished playing")

	except: print(RED + "uh oh" + RESET)

async def addQueue(ctx: discord.ApplicationContext, youtube_link):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		title = await getPageTitle(youtube_link)

		if instance.audioPlaying:
			instance.audioQueue.append(youtube_link)
			await ctx.respond("Added `%s` to queue!"%title)
		else:
			await ctx.respond("No player instance exists. use `play_audio` instead")
	else: await ctx.respond("This server has no audio instance")
	

async def removeQueue(ctx, queue_item_number:int):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		await ctx.defer()
		itemTarget = queue_item_number
		
		if itemTarget == -1:
			firstItem = instance.audioQueue[0]
			instance.audioQueue.clear()
			instance.audioQueue.append(firstItem)

		elif (itemTarget >= 1):
			instance.audioQueue.pop(itemTarget)

		await ctx.respond("Removed from the queue")
	else: await ctx.respond("This server has no audio instance")

async def getQueue(ctx):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		if instance.currentAudioLink != None:
			await ctx.defer()
			queueLength = len(instance.audioQueue)
			numEmbeded = 0

			contextOutput = discord.Embed(title="Queue", description="There are currently %s items queued"%str(queueLength), colour=discord.Colour.dark_purple(),)

			contextOutput.add_field(name="", value="%s [playing]"% await getPageTitle(instance.currentAudioLink), inline=False)
			contextOutput.add_field(name="", value="# ============== #", inline=False)

			for song in instance.audioQueue:
				if numEmbeded <= 9:
					songTitle = await getPageTitle(song)
					contextOutput.add_field(name="", value="%s: %s"%(numEmbeded+1, songTitle), inline=False)
					numEmbeded += 1

			contextOutput.set_footer(text="Only up to the next 9 queued items will be shown")
				
			await ctx.respond(embed=contextOutput)

		else:
			await ctx.respond("No queue can possibly exist; audio player is not spawned")
	else: await ctx.respond("This server has no audio instance")

async def stopTrack(ctx):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]
		
		instance.connectedVC.stop()
		await ctx.respond("Skipped track")
	else: await ctx.respond("This server has no audio instance")

async def pauseToggle(ctx):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		isPaused = instance.connectedVC.is_paused()

		if isPaused: instance.connectedVC.resume(); await ctx.respond("Unpaused")
		else: instance.connectedVC.pause(); await ctx.respond("Paused. Use the `pause_play` command again to resume")
	else: await ctx.respond("This server has no audio instance")

async def allowLeave(ctx):
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		await ctx.defer()
		instance.leaveAfterFinish = True

		await ctx.respond("Issued disconnect request")
	else: await ctx.respond("This server has no audio instance")

async def immediateLeave(ctx):
	await ctx.defer()
	GUILD_ID = ctx.guild.id

	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		if instance.connectedVC != None:
			removeFromMemory(GUILD_ID)

			instance.connectedVC.stop()
			await instance.connectedVC.disconnect()

		await ctx.respond("Issued forced disconnect command")
	else: await ctx.respond("This server has no audio instance")

async def getDebugInfo(ctx):
	GUILD_ID = ctx.guild.id
	if (GUILD_ID in instances_in_memory):
		instance = instanceMemory[str(GUILD_ID)]

		contextOutput = discord.Embed(title="Audio Debugger", description="Fritz Audio Debugger", colour=discord.Colour.brand_red(),)

		contextOutput.add_field(name="", value="instance: %s"%str(instance.connectedVC), inline=False)
		if instance.connectedVC != None:
			contextOutput.add_field(name="", value="is_playing: %s"%instance.connectedVC.is_playing(), inline=False)
			contextOutput.add_field(name="", value="is_paused: %s"%instance.connectedVC.is_paused(), inline=False)
		contextOutput.add_field(name="", value="current_file: <%s>"%instance.currentAudioLink, inline=False)
		contextOutput.add_field(name="", value="leaveAfterFinish: %s"%instance.leaveAfterFinish, inline=False)
		contextOutput.add_field(name="", value="queue_length: %s"%str(len(instance.audioQueue)), inline=False)
		contextOutput.add_field(name="", value="instancesInMemory: %s"%(str(instances_in_memory)))
		contextOutput.add_field(name="", value="")

		contextOutput.set_footer(text="Fritz Embedded Audio Debugger (FEAD)")

		await ctx.respond(embed=contextOutput)
	else: await ctx.respond("This server has no audio instance")