# HEY MA, A NEW UPDATE TOOL JUST CAME OUT
# IT'S REALLY COOL
# IT DOES *RECURSION*

import requests, os, json, sys

MAGENTA = "\u001b[1;35m"
YELLOW = "\u001b[33;1m"
RESET = "\u001b[0m"

BASE_URL = "https://raw.githubusercontent.com/psychon-night/Fritz-for-Discord/refs/heads/main/"
PATH = sys.path[0]

os.system(f"wget --show-progress --progress=bar:force https://github.com/psychon-night/Fritz-for-Discord/archive/refs/heads/main.zip && unzip -o main.zip && rm main.zip && yes | cp -r Fritz-for-Discord-main/* . && rm -r Fritz-for-Discord-main")