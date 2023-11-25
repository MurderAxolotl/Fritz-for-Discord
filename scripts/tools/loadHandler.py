""" Run functions in order to get ready to initialize the bot """
import os

def prepBot():
	for file in os.listdir("/home/%s/Documents/Fritz/cache/"%os.getlogin()):
		if "video_cache" in file:
			os.remove("/home/%s/Documents/Fritz/cache/%s"%(os.getlogin(), file))