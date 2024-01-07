from scripts.tools.utility import *
from discord import ApplicationContext, VoiceChannel

from opuslib import Decoder

voiceInstance1 = None
voiceInstance2 = None\

async def bridgeVoiceChannels(ctx:ApplicationContext, bot, c1:int, c2:int):
	v = await bot.fetch_channel(c1)
	voice = await v.connect()

	while True:
		v.send_audio_packet(b'1')

async def bridgeVoiceChannelss(ctx:ApplicationContext, bot, c1:int, c2:int):
	""" Bridge two voice channels """

	global voiceInstance1, voiceInstance2

	await ctx.defer()

	try: 
		voiceInstance1 = await bot.fetch_channel(c1)
		voiceInstance1 = await voiceInstance1.connect()
	except: await ctx.respond("Failed to connect to VC 1"); return -1

	try: 
		voiceInstance2 = await bot.fetch_channel(c2)
		voiceInstance2 = await voiceInstance2.connect()
	except: await ctx.respond("Failed to connect to VC 2"); return -1

	statusMessage = await ctx.respond("Connected! Bridging channels...")

	await asyncio.sleep(1)

	socket1 = voiceInstance1.socket
	socket2 = voiceInstance2.socket

	sink1 = voiceInstance1.sink
	sink2 = voiceInstance2.sink

	print(sink1)

	while True:
		try: socket2.send(socket1.recv(1024))
		except Exception as err: print(str(err)); await asyncio.sleep(1)