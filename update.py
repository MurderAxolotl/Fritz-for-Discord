# HEY MA, A NEW UPDATE TOOL JUST CAME OUT
# IT'S REALLY COOL
# IT DOES *RECURSION*

import requests, os, json, sys

MAGENTA = "\u001b[1;35m"
YELLOW = "\u001b[33;1m"
RESET = "\u001b[0m"

BASE_URL = "https://raw.githubusercontent.com/psychon-night/Fritz-for-Discord/refs/heads/main/" # I didn't know this existed the first time
PATH = sys.path[0]

JSON_TREE = requests.get("https://api.github.com/repos/psychon-night/Fritz-for-Discord/git/trees/main?recursive=1")

jsonTree = json.loads(JSON_TREE.text)

try:
	for entry in jsonTree["tree"]:
		type = entry["type"]
		path = entry["path"]

		if type == "tree": os.system(f"mkdir -p {PATH}/{path}")
		elif type == "blob":
			if ".pyc" in path or ".vscode" in path: continue

			print(f"{YELLOW} DOWNLOADING {MAGENTA}{path}{RESET}")
			os.system(f"wget -q --show-progress --progress=bar:force -o {PATH}/{path} {BASE_URL}/{path}")

	## I don't see why this *wouldn't* work...
except:
	print(jsonTree)