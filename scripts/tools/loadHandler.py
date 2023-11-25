""" Run functions in order to get ready to initialize the bot """
import os

def prepBot():
	for file in os.listdir("/home/lexi/Documents/Fritz/cache/"):
		if "video_cache" in file:
			os.remove("/home/lexi/Documents/Fritz/cache/%s"%file)