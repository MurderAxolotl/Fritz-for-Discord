import os, sys

MAGENTA = "\u001b[1;35m"
YELLOW = "\u001b[33;1m"
RESET = "\u001b[0m"

BASE_URL = "https://raw.githubusercontent.com/psychon-night/Fritz-for-Discord/refs/heads/main/"
PATH = sys.path[0]

os.system(f"wget --show-progress --progress=bar:force https://github.com/psychon-night/Fritz-for-Discord/archive/refs/heads/main.zip")
os.system("unzip -o main.zip")
os.system("rm main.zip")
os.system("/bin/cp -rf Fritz-for-Discord-main/* .")
os.system("rm -r Fritz-for-Discord-main")